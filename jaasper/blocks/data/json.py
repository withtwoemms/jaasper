from prefect.blocks.system import JSON


block = JSON(value={"hello": "world"})

block.save('some-json')
