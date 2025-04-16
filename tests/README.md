This is playground to test on GitHub Actions Selenium UI testing using docker containers. in current implementation two images is used with selenium-standalone-chromium server and pytest test using MOPS framework.

to run it manually, use:

```bash
  cd .. # go to parent directory
  docker compose build
  docker compose up --abort-on-container-exit
```
