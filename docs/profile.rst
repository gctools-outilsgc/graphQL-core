#######################
Profile as a Service
#######################

***************************
Application architecture
***************************

.. image:: /images/PaS-architecture



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
Search criteria fields can be used separately or chained together to .

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

**************************
Image Resource Server API
**************************

The Profile as a Service leverages `PictShare <https://github.com/chrisiaut/pictshare>`_ which is aa multi lingual, open source image hosting application with a simple resizing and upload API.  PictShare is licensed under the `Apache-2.0 License <https://img.shields.io/badge/license-Apache-blue.svg?style=flat)](https://github.com/chrisiaut/pictshare/blob/master/LICENSE>`_




Features
========

* Simple API to upload any image from remote servers to your instance [via URL](#upload-from-url) and [via Base64](#upload-from-base64-string)
* 100% file based - no database needed
* Simple album functions with embedding support
* Converts gif to (much smaller) MP4
* MP4 resizing
* PictShare removes all exif data so you can upload photos from your phone and all GPS tags and camera model info get wiped
* Smart [resize, filter and rotation](#smart-query-system) features
* Duplicates don't take up space. If the exact same images is uploaded twice, the second upload will link to the first
* Detailed traffic and view statistics of your images via 'Pictshare stats <https://github.com/chrisiaut/pictshare_stats>'_

Smart query system
------------------
PictShare images can be changed after upload just by modifying the URL. It works like this:

``https://base.domain/<options>/<image>``

For example: ``https://avatar.gccollab.ca/100x100/negative/b260e36b60.jpg`` will show you the uploaded Image ```b260e36b60.jpg``` but resize it to 100x100 pixels and apply the "negative" filter. The original image on the resource server will stay untouched.

Available options
-----------------
Original URL: ``https://www.pictshare.net/b260e36b60.jpg``

Note: If an option needs a value it works like this: ``optionname_value``. Eg: ``pixelate_10``
If there is an option requested that's not recognized by PictShare it's simply ignored, so this will work: https://www.pictshare.net/pictshare-is-awesome/b260e36b60.jpg and also even this will work: https://www.pictshare.net/b260e36b60.jpg/how-can-this-still/work/

Resizing
^^^^^^^^
+----------------------+---------------+---------------------------------------------------------+
|        Option        |   Parameter   |                      Example URL                        |
+======================+===============+=========================================================+
| <width>x<height>     |   -none-      |  https://pictshare.net/20x20/b260e36b60.jpg             |
+----------------------+---------------+---------------------------------------------------------+
|     forcecesize      |   -none-      |  https://pictshare.net/100x400/forcesize/b260e36b60.jpg |
+----------------------+---------------+---------------------------------------------------------+

Rotating
^^^^^^^^
+----------------------+---------------+---------------------------------------------------------+
|        Option        |   Parameter   |                      Example URL                        |
+======================+===============+=========================================================+
|        left          |   -none-      |  https://pictshare.net/left/b260e36b60.jpg              |
+----------------------+---------------+---------------------------------------------------------+
|        right         |   -none-      |  https://pictshare.net/right/b260e36b60.jpg             |
+----------------------+---------------+---------------------------------------------------------+
|       upside         |   -none-      |  https://pictshare.net/upside/b260e36b60.jpg            |
+----------------------+---------------+---------------------------------------------------------+

Filters
^^^^^^^
+----------------------+------------------+---------------------------------------------------------+
|        Option        |   Parameter      |                      Example URL                        |
+======================+==================+=========================================================+
|      negative        |      -none-      |  https://pictshare.net/negative/b260e36b60.jpg          |
+----------------------+------------------+---------------------------------------------------------+
|      grayscale       |      -none-      |  https://pictshare.net/grayscale/b260e36b60.jpg         |
+----------------------+------------------+---------------------------------------------------------+
|      brightness      |   -255 to 255    |  https://pictshare.net/brightness_100/b260e36b60.jpg    |
+----------------------+------------------+---------------------------------------------------------+
|      edgedetect      |      -none-      |  https://pictshare.net/edgedetect/b260e36b60.jpg        |
+----------------------+------------------+---------------------------------------------------------+
|       smooth         |   -10 to 2048    |  https://pictshare.net/smooth_3/b260e36b60.jpg          |
+----------------------+------------------+---------------------------------------------------------+
|       contrast       |   -100 to 100    |  https://pictshare.net/contrast_40/b260e36b60.jpg       |
+----------------------+------------------+---------------------------------------------------------+
|       pixelate       |     0 to 100     |  https://pictshare.net/pixelate_10/b260e36b60.jpg       |
+----------------------+------------------+---------------------------------------------------------+
|        blur          | -none- or 0 to 5 |  https://pictshare.net/blur/b260e36b60.jpg              |
+----------------------+------------------+---------------------------------------------------------+
|        sepia         |      -none-      |  https://pictshare.net/sepia/b260e36b60.jpg             |
+----------------------+------------------+---------------------------------------------------------+
|       sharpen        |      -none-      |  https://pictshare.net/sharpen/b260e36b60.jpg           |
+----------------------+------------------+---------------------------------------------------------+
|       emboss         |      -none-      |  https://pictshare.net/emboss/b260e36b60.jpg            |
+----------------------+------------------+---------------------------------------------------------+
|        cool          |      -none-      |  https://pictshare.net/cool/b260e36b60.jpg              |
+----------------------+------------------+---------------------------------------------------------+
|        light         |      -none-      |  https://pictshare.net/light/b260e36b60.jpg             |
+----------------------+------------------+---------------------------------------------------------+
|        aqua          |      -none-      |  https://pictshare.net/aqua/b260e36b60.jpg              |
+----------------------+------------------+---------------------------------------------------------+
|        fuzzy         |      -none-      |  https://pictshare.net/fuzzy/b260e36b60.jpg             |
+----------------------+------------------+---------------------------------------------------------+
|        boost         |      -none-      |  https://pictshare.net/boost/b260e36b60.jpg             |
+----------------------+------------------+---------------------------------------------------------+
|        gray          |      -none-      |  https://pictshare.net/gray/b260e36b60.jpg              |
+----------------------+------------------+---------------------------------------------------------+


GIF to MP4
^^^^^^^^^^
+----------------------+---------------+---------------------------------------------------------+
|        Option        |   Parameter   |                      Example URL                        |
+======================+===============+=========================================================+
|         mp4          |   -none-      |  https://www.pictshare.net/mp4/102687fe65.gif           |
+----------------------+---------------+---------------------------------------------------------+
|         raw          |   -none-      |  https://www.pictshare.net/mp4/raw/102687fe65.gif       |
+----------------------+---------------+---------------------------------------------------------+
|       preview        |   -none-      |  https://www.pictshare.net/mp4/preview/102687fe65.gif   |
+----------------------+---------------+---------------------------------------------------------+

MP4 options
^^^^^^^^^^^
+----------------------+---------------+---------------------------------------------------------+
|        Option        |   Parameter   |                      Example URL                        |
+======================+===============+=========================================================+
|        -none-        |   -none-      |  https://www.pictshare.net/65714d22f0.mp4               |
+----------------------+---------------+---------------------------------------------------------+
|         raw          |   -none-      |  https://www.pictshare.net/raw/65714d22f0.mp4           |
+----------------------+---------------+---------------------------------------------------------+
|       preview        |   -none-      |  https://www.pictshare.net/preview/65714d22f0.mp4       |
+----------------------+---------------+---------------------------------------------------------+



You can also combine as many options as you want. Even multiple times! Want your image to be negative, resized, grayscale , with increased brightness and negate it again? No problem: https://pictshare.net/500x500/grayscale/negative/brightness_100/negative/b260e36b60.jpg


Security and privacy
====================
* No exif data is stored on the server, all jpegs get cleaned on upload
