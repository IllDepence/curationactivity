# ActivityStream for Curations

Following the [recent developments](https://github.com/IIIF/discovery/blob/master/source/api/harvest/0.1/index.md) in IIIF Resource Discovery, here's a take on how an ActivityStream for [third party operations](https://github.com/IIIF/discovery/blob/master/source/api/harvest/0.1/activities.md#third-party-operations) might look like in the case of Curations.

## Usage

* set values in `config.ini`
* place Curation files in folder
* run `$python 3 curationactivity.py`

## Example

Given the input

* [curation1.json](https://illdepence.github.io/curationactivity/iiif/curation1.json)
* [curation2.json](https://illdepence.github.io/curationactivity/iiif/curation2.json)

generates an Activity Stream Collection. For each input Curation a AS Collection Page with `Create`, `Reference` and `Offer` activities is created.

* [Collection](https://illdepence.github.io/curationactivity/as/collection.json)
* [CollectionPage](https://illdepence.github.io/curationactivity/as/page-44411e87-2e2a-4bc6-b78e-67d3f8292e7f.json)
* [CollectionPage](https://illdepence.github.io/curationactivity/as/page-80bd04ac-f4a5-48a9-874d-45cbe711dd45.json)

Keeps track of which files it already parsed so the script can be run again and again on a growing collection of Curations.

## Notes

#### Create
Announces the creation of a Curation.

#### Reference
Announces that a certain (part of a) Canvas was referenced in a Curation.

In contrast to [github.com/IIIF/discovery/](https://github.com/IIIF/discovery/blob/master/source/api/harvest/0.1/activities.md#reference), uses `object` and `origin` — the object of the reference action (what is being referenced) and the reference's origin — instead of `target` and `object`.
Furthermore, `Reference` is [defined as an Activity](https://github.com/IllDepence/curationactivity/blob/master/docs/json-ld/context.json).

#### Offer
Offers a Range to be used in the publisher's Manifest. The Range includes a `within` link to the Curation.

## Curation preview

* view Curation 1 with [Curation Viewer](http://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?curation=https://illdepence.github.io/curationactivity/iiif-compatibility/curation1.json) (uses a slightly reduced [JSON file](https://illdepence.github.io/curationactivity/iiif-compatibility/curation1.json) for compatibility reasons)
* view Curation 2 with [Curation Viewer](http://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?curation=https://illdepence.github.io/curationactivity/iiif-compatibility/curation2.json) (uses a slightly reduced [JSON file](https://illdepence.github.io/curationactivity/iiif-compatibility/curation2.json) for compatibility reasons)
