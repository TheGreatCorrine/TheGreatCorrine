"""
fridge_monitor/entities/record.py
--------------------------------
纯领域实体：不依赖任何框架，只描述“冰箱测试采样点”数据本身
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Dict, Any


@dataclass(slots=True, frozen=True)
class Record:
    """
    一条采样记录（原始点或 1-min 聚合点）

    Attributes
    ----------
    run_id   : str        # 本次试验唯一 ID（上层生成并注入）
    ts       : datetime   # 采样时间；统一使用 **UTC aware** datetime
    metrics  : dict       # 所有模拟 / 数字量键值
    file_pos : int | None # （可选）该记录在源 .dat 中的字节偏移
    """
    run_id: str
    ts: datetime
    metrics: Dict[str, float | int] = field(default_factory=dict)
    file_pos: int | None = None      # 方便做增量解析；不用可删

    # ---------- 工具方法 --------------------------------------------------

    @staticmethod
    def from_dict(
        d: Dict[str, Any],
        *,
        run_id: str,
        file_pos: int | None = None,
    ) -> "Record":
        """
        把解析出的裸 dict 转为 Record。
        要求字典里必须有 `Time_iso`（ISO-8601 字符串）。

        其它所有键值都进 metrics。
        """
        try:
            # 示例格式： "2025-06-20 08:49:25" 或带时区
            ts = datetime.fromisoformat(str(d.pop("Time_iso"))).astimezone(
                timezone.utc
            )
        except KeyError:
            raise ValueError("Expecting key 'Time_iso' in parsed dict")

        # 去掉解析层可能塞进来的临时字段
        d.pop("Timestamp", None)
        d.pop("Time", None)
        d.pop("run_id", None)

        return Record(
            run_id=run_id,
            ts=ts,
            metrics=d,
            file_pos=file_pos,
        )

    # ---------- 序列化 ------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        便于写 JSON / CSV / 返回 API。
        - ts 转成 ISO-8601 字符串
        - metrics 展平到顶层（可选：也可保留嵌套）
        """
        base = {
            "run_id": self.run_id,
            "ts": self.ts.isoformat(),
            **self.metrics,
        }
        if self.file_pos is not None:
            base["file_pos"] = self.file_pos
        return base

    # ---------- 便捷查询 ----------------------------------------------------

    def get(self, key: str, default: float | int | None = None):
        """快捷访问某通道值；等价 metrics.get()"""
        return self.metrics.get(key, default)
