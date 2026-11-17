# 软件许可证并发席位与离线租约

企业软件资产员使用本工具回放在线会话与离线授权，复核峰值席位和超用责任。

## 核心计算

按租约有效区间扫线统计并发，同刻先结束后开始；离线到期前始终占席，重复心跳不重复占用。

## 启动

```bash
docker compose up --build -d
docker compose exec -T app pytest -q
docker compose config --quiet
```

浏览器访问 http://localhost:18214 。默认载入仓内样例。工具条可选择CSV文件运行；样例文件位于 `sample_data/instrument.csv`。重复执行同一内容复用同一批次。

## 模块

- M1 会话接收：`/module/1`，独立计算 `POST /api/1`。
- M2 产品映射：`/module/2`，独立计算 `POST /api/2`。
- M3 租约裁决：`/module/3`，独立计算 `POST /api/3`。
- M4 并发扫描：`/module/4`，独立计算 `POST /api/4`。
- M5 超用归属：`/module/5`，独立计算 `POST /api/5`。
- M6 采购对照：`/module/6`，独立计算 `POST /api/6`。
- M7 补传审计：`/module/7`，独立计算 `POST /api/7`。

## 输入与输出

CSV可用UTF-8或GB18030；上传保留字符串编号和物理行号。POST `/api/run` 接收 `text` 字段。`GET /api/runs` 查询历史，`POST /api/review` 接收 id、revision、decision。导出按钮下载唯一证据CSV，含运行摘要与隔离记录。

SQLite命名卷保存运行记录。重建演示数据可更换卷名后重启。无需外部网络数据。规则定义见 `docs/DATA-DICTIONARY.md`；边界和测试对应关系见 `docs/DEPTH.md`。

## 范围

只处理仓内CSV定义，不连接生产系统。单次输入最多2MB。原始输入流式解析，业务计算阶段需容纳该文件的采信行。并非无限容量任务。
