# JPG-Ayu Profile README

This repository follows the same architecture as the referenced `gargibhardwaj24/gargibhardwaj24` profile repository: self-hosted SVG assets, Python generators, three GitHub Actions workflows, a PowerShell setup helper, dark/light assets, radar charts, contribution metrics, snake animation and generated project/stat cards.

## 1. Put your photo in the repo

Add a file named `me.jpg` to the repository root.

Then run:

```powershell
.\setup.ps1 -Username JPG-Ayu -Name "Ayush Singh" -Image .\me.jpg -Circle
```

## 2. GitHub repository

The profile repository must be named exactly:

`JPG-Ayu/profile`

It should be public.

## 3. Actions permissions

In GitHub:

**Settings → Actions → General → Workflow permissions**

Choose:

**Read and write permissions**

## 4. Metrics token

The metrics workflow uses `secrets.METRICS_TOKEN`.

Create a suitable GitHub token with the permissions needed for the metrics workflow and add it under:

**Settings → Secrets and variables → Actions → New repository secret**

Name:

`METRICS_TOKEN`

Never put a token directly in README.md or any committed file.

## 5. Run workflows

Open **Actions** and manually run:

- `Charts and cards`
- `Metrics`
- `Snake`

The workflows also run automatically on their schedules.

## 6. Add real projects

Edit:

`assets/projects.json`

Only add repositories that actually exist on your GitHub account. The current file contains your public `profile` repository and does not invent projects.

## 7. Update skill radar

Edit:

`assets/skills.json`

Values are 0–100. Then push the change; `radar.yml` regenerates the charts.

## Files

- `README.md` — profile presentation
- `.github/workflows/metrics.yml` — contribution metrics
- `.github/workflows/snake.yml` — contribution snake
- `.github/workflows/radar.yml` — radars and self-hosted cards
- `scripts/dotify.py` — portrait generator
- `scripts/radar.py` — radar generator
- `scripts/cards.py` — stats/project card generator
- `assets/skills.json` — self-rated radar data
- `assets/projects.json` — selected project data
- `setup.ps1` — local asset generator
- `preview.html` — local preview
