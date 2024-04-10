[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/nfa-vfxim/tk-houdini-usdrop?include_prereleases)](https://github.com/nfa-vfxim/tk-houdini-usdrop) 
[![GitHub issues](https://img.shields.io/github/issues/nfa-vfxim/tk-houdini-usdrop)](https://github.com/nfa-vfxim/tk-houdini-usdrop/issues) 


# USD ROP Node <img src="icon_256.png" alt="Icon" height="24"/>

Support for the Toolkit USD ROP node in Houdini.

> Supported engines: tk-houdini

## Requirements

| ShotGrid version | Core version | Engine version |
|------------------|--------------|----------------|
| -                | v0.12.5      | v1.7.1         |

**ShotGrid fields:** -

**Frameworks:** -

## Configuration

### Templates

| Name                      | Description                                                                                                                                      | Default value | Fields                    |
|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|---------------|---------------------------|
| `work_file_template`      | A reference to a template which locates a Houdini work file on disk. This is used to drive the version and optionally the name of output files.
 |               | context, version, [name]  |
| `output_publish_template` | A reference to a template which defines where the published bgeo cache will be copied to.
                                                       |               | context, version, name, * |


