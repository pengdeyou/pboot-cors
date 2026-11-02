<div align="center">
  <img src="docs/_static/pboot-logo.svg" alt="Pboot" height="120">
</div>

# pboot-cors

**pboot-cors** 是 [Pboot](https://gitee.com/pboot-org/pboot) 的跨域资源共享（CORS）扩展。

基于 [flask-cors](https://github.com/corydolphin/flask-cors) 4.0.1 移植，
API 与配置项保持一致，仅将框架依赖从 `flask` 换为 `pboot`。

## 安装

```console
$ pip install pboot-cors
```

## 用法

### 全局启用

```python
from pboot import Pboot
from pboot_cors import CORS

app = Pboot(__name__)

CORS(app, resources={r"/api/*": {
    "origins": "*",
    "allow_headers": ["Content-Type", "Authorization"],
    "expose_headers": ["Content-Disposition"],
    "supports_credentials": False,
}})
```

### 装饰器

```python
from pboot_cors import cross_origin

@app.route("/api/data")
@cross_origin(origins="*")
def data():
    return {"ok": True}
```

## 与 flask-cors 的差异

| 项目 | flask-cors | pboot-cors |
| --- | --- | --- |
| 导入名 | `from flask_cors import CORS` | `from pboot_cors import CORS` |
| 框架依赖 | `flask` | `pboot>=3.2.0` |
| 配置项 | `CORS_*` | `CORS_*`（完全一致） |
| 内部标记 | `_FLASK_CORS_EVALUATED` | `_PBOOT_CORS_EVALUATED` |

配置项、`CORS(app, ...)` 参数、`cross_origin` 装饰器行为均与 flask-cors 一致，
可直接参考其文档。

## 许可证

MIT，详见 [LICENSE](LICENSE)。

上游项目 flask-cors 由 Cory Dolphin 开发，MIT 协议，版权归原作者所有。
