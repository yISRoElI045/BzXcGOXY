# 代码生成时间: 2025-10-13 03:34:23
from dash import Dash, html, dcc, Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
# NOTE: 重要实现细节
import pandas as pd
# TODO: 优化性能

# 初始化Dash应用
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定义页面布局
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    dbc.FormGroup(
                        [
                            dbc.Label("License ID"),
                            dbc.Input(type="text", id="license-id-input"),
                        ]
# FIXME: 处理边界情况
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("License Owner"),
                            dbc.Input(type="text", id="license-owner-input"),
                        ]
                    ),
# NOTE: 重要实现细节
                    dbc.Button("Add License", id="add-license-button", color="primary"),
                ],
                md=6,
            )
        ),
# 添加错误处理
        dbc.Row(
            dbc.Col(
                [
                    dcc.Table(id="license-table"),
                ],
                md=12,
            )
        ),
    ],
    fluid=True,
)

# 许可证数据的内部存储
licenses_db = pd.DataFrame(columns=["License ID", "License Owner"])
# 添加错误处理

# 回调函数，处理添加许可证的逻辑
@app.callback(
    Output("license-table", "data"),
    [Input("add-license-button", "n_clicks")],
    [State("license-id-input", "value"), State("license-owner-input", "value")],
)
def add_license(n_clicks, license_id, owner):
# 增强安全性
    if n_clicks is None or license_id is None or owner is None:
        raise PreventUpdate
# NOTE: 重要实现细节
    try:
        # 将新的许可证添加到DataFrame中
# 改进用户体验
        new_license = pd.DataFrame(
            {
                "License ID": [license_id],
# 添加错误处理
                "License Owner": [owner],
# FIXME: 处理边界情况
            }
        )
        # 检查许可证ID是否已存在
# 添加错误处理
        if not licenses_db[licenses_db["License ID"] == license_id].empty:
            raise ValueError("License ID already exists.")
# FIXME: 处理边界情况
        # 更新许可证数据库
        licenses_db = pd.concat([licenses_db, new_license], ignore_index=True)
    except Exception as e:
        # 错误处理
# FIXME: 处理边界情况
        return [{'License ID': 'Error', 'License Owner': str(e)}]
# NOTE: 重要实现细节
    return licenses_db.to_dict('records')

# 启动服务器
if __name__ == '__main__':
    app.run_server(debug=True)
