# Результаты тестирования с помощью wrk

- Отдача статического документа напрямую через nginx

```bash
  wrk -c 100 -d 10s -t 4 http://localhost:80/static/js/scripts.js   
Running 10s test @ http://localhost:80/static/js/scripts.js
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    14.08ms    2.18ms  36.20ms   91.63%
    Req/Sec     1.78k   266.36     6.58k    93.77%
  71198 requests in 10.10s, 32.52MB read
Requests/sec:   7046.45
Transfer/sec:      3.22MB
```

---
- Отдача статического документа напрямую через gunicorn

```bash
  wrk -c 100 -d 10s -t 4 http://localhost:8081/static/js/scripts.js
Running 10s test @ http://localhost:8081/static/js/scripts.js
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   145.74ms  162.58ms   1.99s    96.29%
    Req/Sec   190.98     29.93   323.00     80.90%
  7616 requests in 10.06s, 33.01MB read
  Socket errors: connect 0, read 0, write 0, timeout 23
  Non-2xx or 3xx responses: 7616
Requests/sec:    757.05
Transfer/sec:      3.28MB
```

---
- Отдача динамического документа напрямую через gunicorn

```bash
  wrk -c 100 -d 10s -t 4 http://localhost:8081/       
Running 10s test @ http://localhost:8081/
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.41s   318.60ms   1.63s    89.29%
    Req/Sec    12.73      6.73    39.00     66.03%
  477 requests in 10.10s, 18.55MB read
  Socket errors: connect 0, read 0, write 0, timeout 10
Requests/sec:     47.23
Transfer/sec:      1.84MB
```

---
- Отдача динамического документа через проксирование запроса с nginx на gunicorn

```bash
    wrk -c 100 -d 10s -t 4 http://localhost:80/  
Running 10s test @ http://localhost:80/
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.06s   543.40ms   2.00s    58.62%
    Req/Sec    12.64      7.10    40.00     74.91%
  472 requests in 10.02s, 18.37MB read
  Socket errors: connect 0, read 0, write 0, timeout 385
Requests/sec:     47.09
Transfer/sec:      1.83MB
```

---
- Отдача динамического документа через проксирование запроса с nginx на gunicorn, при кэшировние ответа на nginx (proxy cache)

```bash
    wrk -c 100 -d 10s -t 4 http://localhost:80/       
Running 10s test @ http://localhost:80/
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    57.62ms  192.86ms   1.96s    95.47%
    Req/Sec     1.20k   371.91     2.63k    80.27%
  44340 requests in 10.07s, 1.69GB read
  Socket errors: connect 0, read 0, write 0, timeout 41
Requests/sec:   4404.41
Transfer/sec:    171.56MB
```

---
## Вывод

При отдаче статических документов nginx превосходит gunicorn по скорости примерно в 10 раз.
При отдаче динамики без кэшрования nginx не дает преимущества, но при включенном кэшировании ускоряет отдачу страниц в 19 раз.
Круто, реально респект!