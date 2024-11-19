from datetime import datetime

from prefect.blocks.system import DateTime


block = DateTime(value=datetime.utcnow())

block.save(name='point-in-time')
