# Usage

* set values in `config.ini`
* run `$python 3 curationactivity.py`

# Example

Given the input

* [curation1.json](https://illdepence.github.io/curationactivity/iiif/curation1.json)
* [curation2.json](https://illdepence.github.io/curationactivity/iiif/curation2.json)

generates an Activity Stream Collection. For each input Curation a AS Collection Page with `Create`, `Reference` and `Offer` activities is created.

* [Collection](https://illdepence.github.io/curationactivity/as/collection.json)
* [CollectionPage](https://illdepence.github.io/curationactivity/as/page-57512cdb-4249-45e8-8df7-bb0c0d422389.json)
* [CollectionPage](https://illdepence.github.io/curationactivity/as/page-6e3b04a4-4708-428b-8012-e30194017370.json)

Also keeps track of which files it already parsed so the script can be run again and again on a growing collection of Curations.

## Curation preview

* view Curation 1 with [Curation Viewer](codh.rois.ac.jp/software/iiif-curation-viewer/demo/?curation=https://illdepence.github.io/curationactivity/iiif-compatibility/curation1.json) (uses a slightly reduced [JSON file](https://illdepence.github.io/curationactivity/iiif-compatibility/curation1.json) for compatibility reasons)
* view Curation 2 with [Curation Viewer](codh.rois.ac.jp/software/iiif-curation-viewer/demo/?curation=https://illdepence.github.io/curationactivity/iiif-compatibility/curation2.json) (uses a slightly reduced [JSON file](https://illdepence.github.io/curationactivity/iiif-compatibility/curation2.json) for compatibility reasons)
