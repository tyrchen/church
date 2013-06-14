Church Basic Idea
=====================

## Thoughts

Church is to replace the excel table in the shared folder which is hard to update and maintain. The engineer just need
to update the PR with comments, color, without needing to fill in with PR number, synopsis, Problem level
(they're automatically populated). Closed PR will be automatically rolled out; PR status change will automatically
reflect in the table.

The purpose is to make engineer to do as less work as possible for this routine work.


## Implementation

* Data source of church is from gnats. A internal spider automatically crawls stakeholders' PR every 4 hours.
* A nodejs backend is used for providing api for the data.
* A django app is used to provide views.

