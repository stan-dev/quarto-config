import pathlib
import argparse


TEMPLATE = """<!DOCTYPE html>
<html lang="en-US">
  <meta charset="utf-8">
  <title>Redirecting&hellip;</title>
  <link rel="canonical" href="{REDIRECT_TO}">
  <script>location="{REDIRECT_TO}"</script>
  <meta http-equiv="refresh" content="0; url={REDIRECT_TO}">
  <meta name="robots" content="noindex">
  <h1>Redirecting&hellip;</h1>
  <a href="{REDIRECT_TO}">Click here if you are not redirected.</a>
</html>
"""

arguments = argparse.ArgumentParser()
arguments.add_argument("redirects_file", type=pathlib.Path)
arguments.add_argument(
    "--output_dir", type=pathlib.Path, default=pathlib.Path(__file__).parent
)

args = arguments.parse_args()

redirects = args.redirects_file.read_text().strip()
out = args.output_dir


for line in redirects.split("\n"):
    if line.startswith("#"):
        continue

    FROM, TO = line.split()
    content = TEMPLATE.format(REDIRECT_TO=TO)

    path = FROM.removeprefix("https://mc-stan.org/")

    file = out / path
    if file.exists():
        print(f"Skipping {file} as it already exists")
        continue

    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content)
