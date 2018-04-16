##############
Core Endpoints
##############
*************
Querying Data
*************

Profile Info
=============
User profile information can be returned fromthis query includes:

* gcId `unique user identifier`
* name `string`
* email `string`
* avatar link `url`
* english position title `string`
* french position title `string`
* mobile phone number `string`
* office phone number `string`
* supervisor `object id pointing to another users gcId`
* organizational group `organization group object id`

    * english organization name `string`
    * french organization name `string`
    * organizational group owner `object id pointing to a gcId`
    * organization `organization object id`

        * organization english name `string`
        * organization french name `string`
        * organization english acronym `string`
        * organization french acronym `string`

* address
    * street address `string`
    * city `string`
    * province `string`
    * postal code `string`
    * country `string`

example of a simple query and a request for a full data set return:

`query{


