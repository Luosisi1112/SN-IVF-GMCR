import pandas as pd
import os
import json
import io
import numpy as np

def detect_initial_issues(file_path):
    """
    检测初始文件的问题
    
    参数:
        file_path: 偏好文件的路径
    
    返回:
        dict: 检测结果
    """
    print("开始检测初始文件...")
    issues = []
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        issues.append(f"文件不存在: {file_path}")
        return {"issues": issues, "data_blocks": []}
    
    # 读取整个文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 根据空行分隔数据块
    data_blocks = []
    current_block = []
    
    lines = content.strip().split('\n')
    empty_line_count = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            empty_line_count += 1
            if empty_line_count >= 2 and current_block:
                data_blocks.append(current_block)
                current_block = []
            continue
        
        empty_line_count = 0
        current_block.append(line)
    
    if current_block:
        data_blocks.append(current_block)
    
    print(f"找到 {len(data_blocks)} 个数据块")
    
    # 检测每个数据块
    for i, block in enumerate(data_blocks):
        print(f"检测数据块 {i+1}...")
        
        # 检查数据块是否为空
        if not block:
            issues.append(f"数据块 {i+1} 为空")
            continue
        
        # 检查数据块是否包含多个矩阵
        header_count = 0
        for line in block:
            if line.startswith('DM,'):
                header_count += 1
        
        if header_count > 1:
            issues.append(f"数据块 {i+1} 包含 {header_count} 个矩阵，可能会被合并解析")
        
        # 尝试解析数据块
        try:
            csv_content = '\n'.join(block)
            df = pd.read_csv(io.StringIO(csv_content))
            print(f"  - 成功解析 {len(df)} 行数据")
            
            # 检查列名
            if 'DM' not in df.columns:
                issues.append(f"数据块 {i+1} 缺少 'DM' 列")
            if 's1' not in df.columns:
                issues.append(f"数据块 {i+1} 缺少 's1' 列")
                
        except Exception as e:
            issues.append(f"解析数据块 {i+1} 时出错: {str(e)}")
    
    return {"issues": issues, "data_blocks": data_blocks}

def parse_preferences_file(file_path):
    """
    解析偏好文件，将其分割为多个数据块并转换为dataframes
    
    参数:
        file_path: 偏好文件的路径
    
    返回:
        dict: 包含所有决策者偏好矩阵的字典
    """
    # 读取整个文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 根据空行分隔数据块（多个连续空行视为一个分隔符）
    data_blocks = []
    current_block = []
    
    lines = content.strip().split('\n')
    empty_line_count = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            empty_line_count += 1
            # 当遇到两个或更多空行时，认为是数据块分隔符
            if empty_line_count >= 2 and current_block:
                data_blocks.append(current_block)
                current_block = []
            continue
        
        empty_line_count = 0  # 重置空行计数
        current_block.append(line)
    
    # 添加最后一个数据块
    if current_block:
        data_blocks.append(current_block)
    
    print(f"找到 {len(data_blocks)} 个数据块")
    
    # 解析每个数据块
    all_dataframes = {}
    decision_makers = ['G', 'M1', 'M2', 'M3', 'R1', 'R2', 'R3']
    
    for i, block in enumerate(data_blocks):
        if not block:
            continue
        
        # 获取决策者名称（如果数量匹配）
        base_dm_name = decision_makers[i] if i < len(decision_makers) else f"DM_{i+1}"
        
        print(f"处理数据块 {i+1}，基础标记为 {base_dm_name}")
        
        # 检查数据块中是否包含多个矩阵（多个表头行）
        header_indices = []
        for j, line in enumerate(block):
            if line.startswith('DM,'):
                header_indices.append(j)
        
        if len(header_indices) > 1:
            # 数据块包含多个矩阵
            print(f"  - 发现 {len(header_indices)} 个矩阵")
            for k, header_idx in enumerate(header_indices):
                # 确定当前矩阵的结束位置
                if k < len(header_indices) - 1:
                    end_idx = header_indices[k+1]
                    matrix_lines = block[header_idx:end_idx]
                else:
                    matrix_lines = block[header_idx:]
                
                # 为每个矩阵创建唯一的决策者名称
                dm_name = f"{base_dm_name}{k+1}" if k > 0 else base_dm_name
                
                print(f"  - 处理矩阵 {k+1}，标记为 {dm_name}")
                
                # 解析CSV格式数据
                try:
                    # 创建临时CSV字符串
                    csv_content = '\n'.join(matrix_lines)
                    
                    # 使用pandas读取
                    df = pd.read_csv(io.StringIO(csv_content))
                    
                    print(f"    - 成功解析 {len(df)} 行数据")
                    
                    # 检查是否有正确的列名
                    if 'DM' in df.columns and 's1' in df.columns:
                        all_dataframes[dm_name] = df
                    else:
                        print(f"    - 警告: 矩阵 {k+1} 不包含预期的列名")
                        
                except Exception as e:
                    print(f"    - 解析矩阵 {k+1} 时出错: {str(e)}")
        else:
            # 数据块只包含一个矩阵
            dm_name = base_dm_name
            
            print(f"  - 处理单个矩阵，标记为 {dm_name}")
            
            # 解析CSV格式数据
            try:
                # 创建临时CSV字符串
                csv_content = '\n'.join(block)
                
                # 使用pandas读取
                df = pd.read_csv(io.StringIO(csv_content))
                
                print(f"  - 成功解析 {len(df)} 行数据")
                
                # 检查是否有正确的列名
                if 'DM' in df.columns and 's1' in df.columns:
                    all_dataframes[dm_name] = df
                else:
                    print(f"  - 警告: 数据块不包含预期的列名")
                    
            except Exception as e:
                print(f"  - 解析数据块时出错: {str(e)}")
    
    return all_dataframes

def save_to_excel(dataframes, output_file):
    """
    将修复后的偏好矩阵保存到Excel文件
    
    参数:
        dataframes: 包含所有决策者偏好矩阵的字典
        output_file: 输出Excel文件的路径
    """
    # 创建Excel写入器
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        # 为每个决策者创建sheet
        for dm, df in dataframes.items():
            df.to_excel(writer, sheet_name=dm, index=False)
            print(f"已保存 {dm} 的数据到sheet: {dm}")
        
        # 创建汇总sheet
        if dataframes:
            all_data = []
            for dm, df in dataframes.items():
                # 添加决策者标识列
                df_copy = df.copy()
                df_copy['决策者'] = dm
                all_data.append(df_copy)
            
            # 合并所有数据
            summary_df = pd.concat(all_data, ignore_index=True)
            
            # 调整列顺序，将决策者列移到前面
            cols = summary_df.columns.tolist()
            cols = cols[-1:] + cols[:-1]  # 将最后一列（决策者）移到前面
            summary_df = summary_df[cols]
            
            summary_df.to_excel(writer, sheet_name='汇总', index=False)
            print("已创建汇总sheet")
    
    print(f"\nExcel文件已成功导出: {output_file}")
    print(f"包含 {len(dataframes)} 个决策者的数据")

def fix_ivfpr_matrix(df):
    """
    修复IVFPR矩阵，使用上三角元素来修复下三角元素，确保满足所有条件：
    1. 0 ≤ l^k_{ij} ≤ u^k_{ij} ≤ 1
    2. l^k_{ij} + u^k_{ji} = 1, u^k_{ij} + l^k_{ji} = 1
    3. l^k_{ii} = u^k_{ii} = 0.5
    
    参数:
        df: 包含偏好矩阵的 dataframe
    
    返回:
        dataframe: 修复后的偏好矩阵
    """
    # 提取状态名称
    states = df.columns.tolist()
    if 'DM' in states:
        states.remove('DM')
    
    n = len(states)
    
    # 创建深拷贝以避免修改原数据
    fixed_df = df.copy(deep=True)
    
    # 创建临时矩阵来存储解析后的值
    l_matrix = np.zeros((n, n))
    u_matrix = np.zeros((n, n))
    
    # 首先解析所有值
    for i, state_i in enumerate(states):
        for j, state_j in enumerate(states):
            cell_value = df.loc[i, state_j]
            if isinstance(cell_value, str) and '[' in cell_value and ']' in cell_value:
                try:
                    val_str = cell_value.strip('[]')
                    l, u = map(float, val_str.split(','))
                    l_matrix[i, j] = l
                    u_matrix[i, j] = u
                except:
                    # 如果解析失败，设为默认值
                    l_matrix[i, j] = 0.0
                    u_matrix[i, j] = 0.0
            else:
                # 如果格式不正确，设为默认值
                l_matrix[i, j] = 0.0
                u_matrix[i, j] = 0.0
    
    # 修复矩阵
    for i, state_i in enumerate(states):
        for j, state_j in enumerate(states):
            if i == j:
                # 条件3: 对角线元素设为0.5
                l = 0.5
                u = 0.5
            elif i > j:
                # 条件2: 下三角元素由上三角元素计算得出
                # l_ij = 1 - u_ji, u_ij = 1 - l_ji
                l = 1.0 - u_matrix[j, i]
                u = 1.0 - l_matrix[j, i]
            else:
                # 上三角元素保持不变，但确保满足条件1
                l = l_matrix[i, j]
                u = u_matrix[i, j]
                # 确保 0 ≤ l ≤ u ≤ 1
                l = max(0.0, min(1.0, l))
                u = max(0.0, min(1.0, u))
                if l > u:
                    # 如果l > u，调整为合理值
                    u = max(u, l)
            
            # 确保 0 ≤ l ≤ u ≤ 1
            l = max(0.0, min(1.0, l))
            u = max(0.0, min(1.0, u))
            if l > u:
                u = l
            
            # 更新修复后的值
            fixed_df.loc[i, state_j] = f"[{l:.6f}, {u:.6f}]"
    
    return fixed_df

def check_ivfpr_conditions(dataframes):
    """
    检查每个偏好矩阵是否满足IVFPR的条件：
    1. 0 ≤ l^k_{ij} ≤ u^k_{ij} ≤ 1
    2. l^k_{ij} + u^k_{ji} = 1, u^k_{ij} + l^k_{ji} = 1
    3. l^k_{ii} = u^k_{ii} = 0.5
    
    参数:
        dataframes: 包含所有决策者偏好矩阵的字典
    
    返回:
        dict: 每个决策者的检查结果
    """
    results = {}
    
    for dm, df in dataframes.items():
        print(f"\n检查决策者 {dm} 的偏好矩阵...")
        
        # 提取状态名称
        states = df.columns.tolist()
        if 'DM' in states:
            states.remove('DM')
        
        n = len(states)
        errors = []
        
        # 创建偏好矩阵的下界和上界矩阵
        l_matrix = np.zeros((n, n))
        u_matrix = np.zeros((n, n))
        
        # 填充矩阵
        for i, state_i in enumerate(states):
            for j, state_j in enumerate(states):
                # 提取偏好值（假设格式为 [l, u]）
                cell_value = df.loc[i, state_j]
                if isinstance(cell_value, str) and '[' in cell_value and ']' in cell_value:
                    # 解析区间值
                    try:
                        val_str = cell_value.strip('[]')
                        l, u = map(float, val_str.split(','))
                        l_matrix[i, j] = l
                        u_matrix[i, j] = u
                    except Exception as e:
                        errors.append(f"状态 {state_i} 到 {state_j} 的偏好值格式错误: {cell_value}")
                        continue
                else:
                    errors.append(f"状态 {state_i} 到 {state_j} 的偏好值格式错误: {cell_value}")
                    continue
        
        # 检查条件1: 0 ≤ l ≤ u ≤ 1
        for i in range(n):
            for j in range(n):
                l = l_matrix[i, j]
                u = u_matrix[i, j]
                if l < 0 or l > 1:
                    errors.append(f"状态 {states[i]} 到 {states[j]} 的下界 {l} 不在 [0,1] 范围内")
                if u < 0 or u > 1:
                    errors.append(f"状态 {states[i]} 到 {states[j]} 的上界 {u} 不在 [0,1] 范围内")
                if l > u:
                    errors.append(f"状态 {states[i]} 到 {states[j]} 的下界 {l} 大于上界 {u}")
        
        # 检查条件2: 互反性
        for i in range(n):
            for j in range(n):
                if i != j:
                    l_ij = l_matrix[i, j]
                    u_ij = u_matrix[i, j]
                    l_ji = l_matrix[j, i]
                    u_ji = u_matrix[j, i]
                    
                    # 检查 l_ij + u_ji = 1
                    if abs(l_ij + u_ji - 1) > 1e-6:
                        errors.append(f"状态 {states[i]} 到 {states[j]} 和 {states[j]} 到 {states[i]} 不满足 l_ij + u_ji = 1: {l_ij} + {u_ji} = {l_ij + u_ji}")
                    
                    # 检查 u_ij + l_ji = 1
                    if abs(u_ij + l_ji - 1) > 1e-6:
                        errors.append(f"状态 {states[i]} 到 {states[j]} 和 {states[j]} 到 {states[i]} 不满足 u_ij + l_ji = 1: {u_ij} + {l_ji} = {u_ij + l_ji}")
        
        # 检查条件3: 自反性
        for i in range(n):
            l_ii = l_matrix[i, i]
            u_ii = u_matrix[i, i]
            if abs(l_ii - 0.5) > 1e-6:
                errors.append(f"状态 {states[i]} 到自身的下界 {l_ii} 不等于 0.5")
            if abs(u_ii - 0.5) > 1e-6:
                errors.append(f"状态 {states[i]} 到自身的上界 {u_ii} 不等于 0.5")
        
        # 保存结果
        if errors:
            print(f"决策者 {dm} 的偏好矩阵不满足IVFPR条件：")
            for error in errors:
                print(f"  - {error}")
            results[dm] = {'valid': False, 'errors': errors}
        else:
            print(f"决策者 {dm} 的偏好矩阵满足所有IVFPR条件")
            results[dm] = {'valid': True, 'errors': []}
    
    return results

if __name__ == "__main__":
    """
    主函数流程：
    1. 定义文件路径
    2. 检测初始文件问题
    3. 解析偏好文件
    4. 修复IVFPR矩阵
    5. 检查修复后的矩阵是否满足条件
    6. 保存修复后的数据到Excel
    """
    # 1. 定义文件路径
    import os
    
    # 使用相对路径，基于当前工作目录
    input_file = os.path.join(os.path.dirname(__file__), "偏好")
    output_file = os.path.join(os.path.dirname(__file__), "processed_preferences.xlsx")
    
    print(f"输入文件路径: {input_file}")
    print(f"输出文件路径: {output_file}")
    
    # 2. 初始文件检测
    print("\n" + "="*60)
    print("步骤1: 检测初始文件")
    print("="*60)
    
    detection_result = detect_initial_issues(input_file)
    
    if detection_result["issues"]:
        print("\n发现以下问题:")
        for issue in detection_result["issues"]:
            print(f"  - {issue}")
    else:
        print("\n初始文件检测未发现明显问题")
    
    # 3. 解析文件
    print("\n" + "="*60)
    print("步骤2: 解析偏好文件")
    print("="*60)
    
    dataframes = parse_preferences_file(input_file)
    
    # 4. 修复IVFPR矩阵
    if dataframes:
        print("\n" + "="*60)
        print("步骤3: 修复IVFPR矩阵")
        print("="*60)
        
        fixed_dataframes = {}
        for dm, df in dataframes.items():
            print(f"\n修复决策者 {dm} 的偏好矩阵...")
            print(f"  - 原始矩阵大小: {df.shape}")
            
            # 展示原始矩阵的部分内容
            print("  - 原始矩阵前2行:")
            print(df.head(2))
            
            # 修复矩阵
            fixed_df = fix_ivfpr_matrix(df)
            fixed_dataframes[dm] = fixed_df
            
            # 展示修复后的部分内容
            print("  - 修复后矩阵前2行:")
            print(fixed_df.head(2))
        
        # 5. 检查修复后的IVFPR条件
        print("\n" + "="*60)
        print("步骤4: 验证修复后的数据")
        print("="*60)
        
        check_results = check_ivfpr_conditions(fixed_dataframes)
        
        # 6. 保存修复后的数据到Excel
        print("\n" + "="*60)
        print("步骤5: 保存修复后的数据")
        print("="*60)
        
        save_to_excel(fixed_dataframes, output_file)
        
        # 7. 最终总结
        print("\n" + "="*60)
        print("最终总结")
        print("="*60)
        
        print(f"成功处理 {len(fixed_dataframes)} 个决策者的数据")
        print(f"Excel文件已成功导出: {output_file}")
        print("\n处理完成！")
    else:
        print("错误：未成功解析任何数据块！")