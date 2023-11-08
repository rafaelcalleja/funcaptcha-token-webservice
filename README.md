--------------------------------------

### Usage

1. make build
2. make run
3. curl -X POST http://0.0.0.0:9000/token?public_key=0A1D34FC-659D-4E23-B17B-694DCFCF6A6C

```js
{
  "token": "5151795b1484940b1.4329825105|r=eu-west-1|meta=3|metabgclr=transparent|metaiconclr=%23757575|guitextcolor=%23000000|pk=0A1D34FC-659D-4E23-B17B-694DCFCF6A6C|at=40|ag=101|cdn_url=https%3A%2F%2Fapi.funcaptcha.com%2Fcdn%2Ffc|lurl=https%3A%2F%2Faudio-eu-west-1.arkoselabs.com|surl=https%3A%2F%2Fapi.funcaptcha.com|smurl=https%3A%2F%2Fapi.funcaptcha.com%2Fcdn%2Ffc%2Fassets%2Fstyle-manager",
  "solve_time": "4s",
  "error": null
}
```
4. http://0.0.0.0:9000/docs
