# Release procedure

1. Determine version based on pandas version tested (a.b.c) and date yymmdd, to make
   version string a.b.c.yymmdd
2. Update `pyproject.toml` and `pandas-stubs/_version.pyi` to have the new version string
3. Execute the following commands:

```shell
rm dist/*
poetry build
twine upload dist/*
git commit -a -m "Version a.b.c.yymmdd"
git push upstream main
git tag va.b.c.yymmdd
git push upstream --tags
```

The conda bots will recognize that a new version has been uploaded to pypi, and generate a pull request sent to the maintainers to approve it.
