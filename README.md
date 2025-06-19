# JCOIN Data Schemas

This repository contains [tabular data schemas](https://datapackage.org/standard/table-schema/) for data packages used by the Justice Community Opioid Innovation Network (JCOIN). A *data schema* provides a formal description of a dataset, including (but not limited to) variable names, types, labels, descriptions, and possible values. It is both human readable but can also be used to perform useful operations such as validating a dataset or controlling the way it is imported into an analytic software package (e.g., Stata, R, or SAS).

The authoratitive schemas are maintained in [JSON](https://en.wikipedia.org/wiki/JSON) format, but may be translated into other formats as well (e.g., CSV).


## JCOIN Core Measures

The *JCOIN core measures* are a set of common data elements collected by all of the JCOIN research hubs. Their schemas are located in the [schemas folder](https://github.com/jcoin-maarc/JCOIN-core-measures/tree/main/schemas/core_measures). It can be convenient to view them using a service such as [JSON Hero](https://github.com/triggerdotdev/jsonhero-web) or [JSON Crack](https://jsoncrack.com) which you may do with the links below:

- Data collected at baseline from research participants ([Hero](https://jsonhero.io/new?url=https://raw.githubusercontent.com/jcoin-maarc/JCOIN-core-measures/refs/heads/main/schemas/core_measures/table-schema-baseline.json), [Crack](https://jsoncrack.com/editor?json=https://raw.githubusercontent.com/jcoin-maarc/JCOIN-core-measures/refs/heads/main/schemas/core_measures/table-schema-baseline.json))
- Data collected longitudinally from research participants ([Hero](https://jsonhero.io/new?url=https://raw.githubusercontent.com/jcoin-maarc/JCOIN-core-measures/refs/heads/main/schemas/core_measures/table-schema-longitudinal.json), [Crack](https://jsoncrack.com/editor?json=https://raw.githubusercontent.com/jcoin-maarc/JCOIN-core-measures/refs/heads/main/schemas/core_measures/table-schema-longitudinal.json))
- Data collected at baseline from staff ([Hero](https://jsonhero.io/new?url=https://raw.githubusercontent.com/jcoin-maarc/JCOIN-core-measures/refs/heads/main/schemas/core_measures/table-schema-staff-baseline.json), [Crack](https://jsoncrack.com/editor?json=https://raw.githubusercontent.com/jcoin-maarc/JCOIN-core-measures/refs/heads/main/schemas/core_measures/table-schema-staff-baseline.json))
- Data collected longitudinally from staff ([Hero](https://jsonhero.io/new?url=https://raw.githubusercontent.com/jcoin-maarc/JCOIN-core-measures/refs/heads/main/schemas/core_measures/table-schema-staff-longitudinal.json), [Crack](https://jsoncrack.com/editor?json=https://raw.githubusercontent.com/jcoin-maarc/JCOIN-core-measures/refs/heads/main/schemas/core_measures/table-schema-staff-longitudinal.json))

In addition to the datasets above, a small administrative dataset is used to record information about each participant's flow throughout the study:

- Administrative data on participants ([Hero](https://jsonhero.io/new?url=https://raw.githubusercontent.com/jcoin-maarc/JCOIN-core-measures/refs/heads/main/schemas/core_measures/table-schema-admin.json), [Crack](https://jsoncrack.com/editor?json=https://raw.githubusercontent.com/jcoin-maarc/JCOIN-core-measures/refs/heads/main/schemas/core_measures/table-schema-admin.json))


## Validating Your Data

Instructions for using these schemas to validate your data may be found [here](https://github.com/jcoin-maarc/JCOIN-core-measures/blob/main/docs/validation.md).
