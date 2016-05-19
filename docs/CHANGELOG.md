# Change log

All notable changes to this project will be documented in this file.


## v0.2.0 - [2016-05-19]
### Added
- `AddressMixin`, `GPSMixin` and `AddressGPSMixin` classes to ease 
  defining address fields within models.
- `altitude` and `gps_error` fields to the `Address` model. These fields 
  are equally present within the GSPMixin.

### Removed
- Reverse navigation from states to addresses in the `Address` model.