*******************
Object Data Models
*******************

User
=====
* ``gcId`` *a unique user identifier* (string)
* ``name`` *user's name* (string)
* ``email`` *user's email* (string)
* ``avatar`` *url to user's profile avatar* (url)
* ``titleEn`` *user's english position title* (string)
* ``titleFr`` *user's french position title* (string)
* ``mobilePhone`` *mobile phone number* (string)
* ``officePhone`` *office phone number* (string)
* ``address`` *user's work address* (address object)
* ``supervisor`` *user object of identified supervisor* (user object)
* ``org`` *organizational tier group object* (org tier object)
* ``Employees`` *array of user objects that have this user as their supervisor* (user object array)
* ``OwnerOfOrgTier`` *array of organizational tier objects that have this user as their owner* (organizational tier array)


Address
========
* ``id`` *unique address object identifier* (int)
* ``streetAddress`` (string)
* ``city`` (string)
* ``province`` (string)
* ``postalCode`` (string)
* ``country`` (string)

Organization Tier
===================
* ``id`` *unique organizaitonal tier object identifier* (int)
* ``nameEn`` *english name of organizational tier* (string)
* ``nameFr`` *french name of organizational tier* (string)
* ``organization`` *top level organization object* (organization object)
* ``ownerID`` *user object of the user who is listed as the owner of this org tier* (user object)
* ``OrgMembers`` *array of user objects who are associated with this org tier* (user object array)

Organization
==============
* ``id`` *unique organization object identifier* (int)
* ``nameEn`` *english name of organization* (string)
* ``nameFr`` *french name of organization* (string)
* ``acronymEn`` *english acronym of the organization* (string)
* ``acronymFr`` *french acronym of the organization* (string)
* ``OrgTiers`` *array of organizational tiers that are associated with this organization* (organizational tier array)

***************
Core Endpoints
***************



/graphiql
===========
This endpoint is used to access the graphiql interface which permits querying into the graphQL core through an easy to understand user interface.  See :ref:`graphiql-reference-label` for available queries and mutations.


.. _graphiql-reference-label:

/graphqlcore
=============
This endpoint is used by client applications that do not require a graphical interface.  This endpoint is a pure API.

Available Queries
--------------------
Queries do not require authentication of the client through the means of an access token.

Base query for all available information of a user without search criteria
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    profiles{
        gcID,
        name,
        email,
        avatar,
        mobilePhone,
        officePhone,
        titleEn,
        titleFr,
        address{
            id,
            streetAddress,
            city,
            province,
            postalCode,
            country
        }
        supervisor{
            gcID,
            name,
            email,
            avatar,
            mobilePhone,
            officePhone,
            titleEn,
            titleFr,
            address{
                id,
                streetAddress,
                city,
                province,
                postalCode,
                country
            }
        }
        org{
            id,
            nameEn,
            nameFr,
            organization{
                id,
                nameEn,
                nameFr,
                acronymEn,
                acronymFr,
            },
            ownerID{
                gcID,
                name,
                email,
                avatar,
                mobilePhone,
                officePhone,
                titleEn,
                titleFr,
                address{
                    id,
                    streetAddress,
                    city,
                    province,
                    postalCode,
                    country
                }
            }
        }
        OwnerOfOrgTier{
            nameEn,
            nameFr,
            organization{
                id,
                nameEn,
                nameFr,
                acronymEn,
                acronymFr,
            },
            OrgMembers{
                gcID,
                name,
                email,
                avatar,
                mobilePhone,
                officePhone,
                titleEn,
                titleFr,
                address{
                    id,
                    streetAddress,
                    city,
                    province,
                    postalCode,
                    country
                }

            }
        }
    }

Query search criteria
^^^^^^^^^^^^^^^^^^^^^^
Search criteria fields can be used separately or together to generate limitless filtering possibilities.

**Profile**

::

    query{
        profiles(
            gcID:"string",
            name:"string",
            email:"string",
            mobilePhone:"string",
            officePhone:"string",
            titleEn:"string",
            titleFr:"string"
        )
    }

**Addresses**

::

    query{
        addresses(
        streetAddress:"string",
        city:"string",
        province:"string",
        postalCode:"string",
        country:"string"
        )
    }

**Organizational Tiers**

::

    query{
        orgtiers(
            nameEn:"string",
            nameFr:"string",
        )
    }

**Organizations**

::

    query{
        organizations(
            nameEn:"string",
            nameFr:"string",
            acronymEn:"string",
            acronymFr:"string"
        )
    }

Paginiation
^^^^^^^^^^^^^^^^

Retrieving too much data on a single request is unpractical and may even break your app. Pagination exists to solve this problem, allowing the client to specify how many items it wants.

The simple way defined in the GraphQL pagination documentation is to slice the results using two parameters: ``first``, which returns the first n items and ``skip``, which skips the first n items.

These two pagination parameters have been implemented on all of the search query functions.

The example query below will search for all profiles that contain the name "Bryan" but instead of returning the complete array the query below is requesting items 2 and 3 in the array.  Skip the first item in the array and send the next 2 in the array.

::

    query{
        profiles(name:"Bryan", first:2, skip:1){
            name,
            avatar,
            email
        }
    }



/protected
============
This endpoint is similar to the ``graphqlcore`` endpoint however is used for data management applications that have access to additional graphQL mutations.  This endpoint is protected by token authentication and requires an account and active token on the graphql-core.

