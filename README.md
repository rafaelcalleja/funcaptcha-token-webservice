--------------------------------------

### Usage

1. make build
2. make run
3. curl -X POST http://0.0.0.0:9000/token?public_key=0A1D34FC-659D-4E23-B17B-694DCFCF6A6C

```js
{
  "token": "5431795b7ae148968.7947221705|r=eu-west-1|meta=3|metabgclr=transparent|metaiconclr=%23757575|guitextcolor=%23000000|pk=0A1D34FC-659D-4E23-B17B-694DCFCF6A6C|at=40|sup=1|rid=49|ag=101|cdn_url=https%3A%2F%2Ftcr9i.chat.openai.com%2Fcdn%2Ffc|lurl=https%3A%2F%2Faudio-eu-west-1.arkoselabs.com|surl=https%3A%2F%2Ftcr9i.chat.openai.com|smurl=https%3A%2F%2Ftcr9i.chat.openai.com%2Fcdn%2Ffc%2Fassets%2Fstyle-manager",
  "challenge_url": "",
  "challenge_url_cdn": "https://tcr9i.chat.openai.com/cdn/fc/assets/ec-game-core/bootstrap/1.15.0/standard/game_core_bootstrap.js",
  "challenge_url_cdn_sri": null,
  "noscript": "Disable",
  "inject_script_integrity": null,
  "inject_script_url": null,
  "mbio": true,
  "tbio": true,
  "kbio": true,
  "styles": [
    {
      "name": "base",
      "theme": "",
      "iframeWidth": null,
      "iframeHeight": null,
      "style": {
        "id": "3223837d-b9be-4434-9472-a11da5009681",
        "sriHash": "sha384-/7CUM1uGhxkHhx+nKi/dbQzeuPzpboUUWVWUypHdmKPYpUQsO4uWHXQYUrgkx2az"
      },
      "assets": {
        "home.logo": "bef94bc0-26f4-4147-8928-854e4e94b4ec.svg"
      }
    }
  ],
  "iframe_width": null,
  "iframe_height": null,
  "disable_default_styling": false,
  "string_table": {
    "meta.api_timeout_error": "Соединение с сервером проверки прервано. Перезагрузите задание и повторите попытку.",
    "meta.generic_error": "Что-то пошло не так. Перезагрузите задание и повторите попытку.",
    "meta.loading_info": "В процессе, подождите...",
    "meta.reload_challenge": "Перезагрузить задание",
    "meta.visual_challenge_frame_title": "Визуальное задание"
  }
}
```
4. http://0.0.0.0:9000/docs
