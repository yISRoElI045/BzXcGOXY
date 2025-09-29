# 代码生成时间: 2025-09-30 03:30:31
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from threading import Thread
import time

# 定义 Dash 应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Progress Indicator App'

# 定义应用布局
app.layout = html.Div([
    html.H1("Progress Bar and Loader Example"),
    html.Div(dbc.Button("Start Progress", id="start-progress", color="primary", n_clicks=0)),
    html.Div(id="progress-container", style={'display': 'none'}),
    dcc.Interval(id='interval-component', interval=100, n_intervals=0),
    html.Div(id='progress-bar-container'),
    html.Div(id='progress-output', style={'display': 'none'})
])

# 定义全局变量以跟踪进度条状态
progress = 0
max_steps = 100

# 定义辅助函数以更新进度条
def update_progress_bar(progress):
    children = [html.Div(className="text", children=f"{progress}%"),
               html.Div(className="bar",
                        style={"width": f"{progress}%"})],
    return dbc.Progress(value=progress, children=children, striped=True, animated=True)

# 定义回调函数以处理进度条更新
@app.callback(
    Output("progress-container", "children"),
    Input("interval-component", "n_intervals"),
    State("start-progress", "n_clicks"),
    State("progress-output", "children")
)
def update_progress(n, start_clicks, progress_output):  # type: ignore
    global progress
    if start_clicks > 0 and progress_output is None:  # 开始进度
        progress += 1
        if progress > max_steps:  # 重置进度
            progress = 0
        # 更新进度条
        return update_progress_bar(progress)
    return None

# 定义回调函数以处理用户点击事件
@app.callback(
    Output("progress-bar-container", "children"),
    prevent_initial_call=True,
    Input("start-progress", "n_clicks"),
    State("progress-bar-container", "children")
)
def display_progress_bar(n_clicks, current_display):  # type: ignore
    if n_clicks > 0 and current_display is None:  # 显示进度条
        return update_progress_bar(0)
    return current_display

# 定义回调函数以显示进度完成信息
@app.callback(
    Output("progress-output", "children"),
    [Input("interval-component", "n_intervals")],
    [State("start-progress", "n_clicks"), State("progress-output", "children")]
)
def show_end_of_progress(n_intervals, n_clicks, progress_output):  # type: ignore
    global progress
    if progress == max_steps and progress_output is None:  # 进度完成
        return html.Div(["Progress completed!"])
    return progress_output

# 定义线程函数以异步更新进度条
def start_progress_thread():  # type: ignore
    global progress
    while True:  # 模拟长时间运行的任务
        time.sleep(0.1)  # 等待0.1秒
        if progress < max_steps:  # 更新进度
            progress += 1
        else:  # 退出循环
            break

# 定义回调函数以处理进度条开始
@app.callback(
    Output("interval-component", "interval"),
    [Input("start-progress", "n_clicks")],
    [State("interval-component", "interval"), State("progress-output", "children")]
)
def start_interval(n_clicks, interval, progress_output):  # type: ignore
    if n_clicks > 0 and progress_output is None:  # 开始进度条
        interval = 100
        # 创建并启动线程
        thread = Thread(target=start_progress_thread)
        thread.start()
    return interval

# 启动 Dash 应用
if __name__ == '__main__':
    app.run_server(debug=True)