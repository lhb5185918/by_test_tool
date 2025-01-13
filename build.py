import os
import shutil
import PyInstaller.__main__
import yaml

# 清理旧的构建文件
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

# 确保配置文件存在
config_files = {
    'config.py': 'config = {}',
    'in_order_data.yaml': {},
    'qc_data.yaml': {},
    'ac_data.yaml': {}
}

for file_name, content in config_files.items():
    if not os.path.exists(file_name):
        if file_name.endswith('.py'):
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            with open(file_name, 'w', encoding='utf-8') as f:
                yaml.safe_dump(content, f)

# 运行PyInstaller
PyInstaller.__main__.run([
    'bytestool.spec',
    '--clean',
    '--noconfirm'
])

print("打包完成！") 