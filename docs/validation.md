# Data Validation

A schema may be used to validate a dataset that conforms to that schema. This ensures that the dataset contains all of the required variables in the right order, that each variable contains only values from its expected range (e.g., integers, strings, dates, or a fixed set of values such as "Yes" or "No"), and that missing values are indicated using one of a set of pre-specified values (e.g., "Don't know" or "Refused").

Validation may be performed using the [Python package `frictionless`](https://pypi.org/project/frictionless/). For those with an existing Python installation, this may be installed in the usual way using `pip`:

    pip install frictionless

For those who do not have Python and would like to install it, the latest version for all major platforms is available for download [here](https://www.python.org/downloads/). However, a better alternative for some may be to use `frictionless` within a JCOIN Data Commons (JDC) workspace. To request access to a workspace, please send an email to [jcoin-support@gen3.org](mailto:jcoin-support@gen3.org).

Two working sessions were held demonstrating how to validate data within a JDC workspace. Recordings of those working sessions may be downloaded from the following links:

- [Working session held 2025-02-20](https://uchicago.box.com/s/q8yfqmfzqp0lwu9dlj1xpsm1qbm8nez8)
- [Working session held 2025-02-25](https://uchicago.box.com/s/l95ab3ohfoa9zszkjpgpwy1lsdfucesx)


## Using Frictionless

Using Frictionless to validate a dataset is easy. For example, suppose you have prepared a file called `mydata.csv` containing the baseline participant data for your hub. Once you have the `frictionless` package installed, open a terminal (e.g., Terminal.app on OS X or **cmd** on Windows) and type

    frictionless validate --schema table-schema-baseline.json mydata.csv

    ───────────────────────── Dataset ─────────────────────────

    ┏━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
    ┃ name          ┃ type  ┃ path                   ┃ status ┃
    ┡━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
    │ mydata.csv    │ table │ mydata.csv             │ VALID  │
    └───────────────┴───────┴────────────────────────┴────────┘

which, in this case, confirms that the data are valid (if there had been problems with the data we would have received brief descriptions of each of the problems).

The command above performs strict validation, which includes verifying that all of the variables are present and in the right order, and that there are no additional variables (i.e., not included in the schema). However, during the process of preparing a dataset, it can be useful to validate from time to time as you go along, in which case the file you are validating may not yet be complete (i.e., may not have all of the variables), may have extraneously (temporary) variables, or may be out of order. To avoid receiving error messages about these minor issues, you may add the `--schema-sync` option to the command above. Be sure, however, to exclude this option when doing a final validation prior to submitting your data.


## Using Frictionless in the JDC

Frictionless has been installed in the JDC workspaces, and you may find it easier to validate your data there instead of installing Python and/or Frictionless locally. To do this:

1. Point your browser to [https://jcoin.datacommons.io](https://jcoin.datacommons.io/) and log in.
2. Click on the Workspace tab at the top right (if you haven't yet requested access to workspaces, please do so by sending an email to [jcoin-support@gen3.org](mailto:jcoin-support@gen3.org)).
3. Launch the workspace named "Jupyter Lab Notebook with R Kernel."
4. Upload your data file (using the up arrow at the top of the file browser on the left) into the `pd` folder (files in this folder are preserved across sessions). Note that your workspace may be accessed only by you; there is no way for another user to access the files you upload.
5. Launch a terminal, and change directory to the location of your uploaded file (using `cd`).
6. Modify the command above as shown:

       frictionless validate --schema https://raw.githubusercontent.com/jcoin-maarc/JCOIN-core-measures/refs/heads/main/schemas/core_measures/table-schema-baseline.json mydata.csv

This reads the schema file directly from GitHub. Alternatively, you may download the schema file from GitHub, upload it into the workspace, and use the same command in the section above.