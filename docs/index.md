
# JCOIN Core Measures Table Schemas/Data Dictionaries

 
This project builds data dictionaries (ie schemas) to represent (and build upon) the publicly available core measures PDF document. The goal of this project is to make machine readable data dictionaries and user-friendly products, allowing easier search and discovery of the JCOIN Core Measure variables for harmonization,analysis, and collaboration. 

## Data model 

- We used an OMOP-consistent data model approach provides more flexibility in converting heterogenous hub source data into a common data model and is amenable to easier analyses

- Currently the two entities (ie., data tables/files) are*: 
    1. Person level – measures collected only at baseline (and current enrollment status) which is called `baseline`
        - note, this may be changed to from "baseline" to "person" in future to account for non-baseline measure in model (current enrollment status)
    2. Person/visit level: measures collected at all timepoints which is called `time-points`


* staff also have baseline and time-points. While most staff will only have one timepoint, we put staff specific items that may be collected across timepoints (eg organizational questions), in `staff-timepoints`


## Data package standards (Frictionless) framework

The frictionless framework plays a foundational component in our Core Measures, both in building upon the core measures and building core measure data packages. For more information on frictionless standards, [click here](https://specs.frictionlessdata.io/). Specifically, the core measure data dictionary relies heavily on the [Table Schema specification](https://specs.frictionlessdata.io/table-schema).


## Core Measure browser

This provides a way to explore the most up-to-date data dictionaries and other dataset metadata properties such as missing values, descriptions, keys, etc. One can also search the complete set of core measures and download a formatted excel version

[Click here for core measure browser](./browser.md){.md-button .md-button--primary }