# 席位定义

lease_id、user保持字符串。CAD-Pro、cad归一为CAD。kind取online、offline、heartbeat、release、capacity。start/end必须带时区并转换UTC。seats为正整数；capacity记录表示采购生效区间的席位上限。

在线租约可由同租约同版本release提前结束；离线授权一直占用至原到期时刻，即使收到release仍保留。心跳不建立租约。租约采用最高版本；同版多条实体租约冲突隔离。采购区间可重叠，最高version优先，同最高版不同数量返回CAPACITY_CONFLICT。

并发使用半开区间[a,b)，结束同刻开始不重叠。采购边界必须切分并发段。超用责任按租约开始时间倒序、再按编号倒序分配，分配席位严格等于超用数量。超用席位小时为超用数量×秒数/3600，Decimal计算。此工具只核验约定席位数，不含厂商复杂许可证条款。

租约ID在产品内唯一；不同产品允许相同租约号。线上租约在start同刻release得到零时占用，离线仍保留原到期。
