# Contributing
If you would like to contribute to this project, follow the guidelines below.

## Issues
When submitting an issue, please use the following guidelines.

#### Issue Titles
Give your issue a concise title that discribes the problem/desired enhancement. For example `Add NPR news parser` or `Improve NPR news parser documentation`.

#### Issue Content
Provide as much detail as possible when submitting new issues so that the team can understand what the problem is and make a plan to address it. A good template is as follows:
```
#### Short description of the problem/feature request

#### Expected behavior

#### Actual behavior (bugs)

#### Minimal example to reproduce the issue (bugs)

#### Code version

#### Affected systems (if relevant)
```

## Branches
We name branches after the type of pull request being made, followed by an issue number and short title: 
`<pr_type>/<issue#>_<short_desctiption>`

Example pull request types include:
* `bugfix`: Used when the PR fixes a bug or other issue
* `enhancement`: Used when the PR improves on existing code
* `doc`: Used when the PR improves on the code by adding to the documentation, fixing a typo, or similar.

## Commits
Strive to [write small, tight commits](http://chris.beams.io/posts/git-commit/) that follow this outline:
```
Summarize changes in 50 characters or less

More detailed explanatory text, if necessary. Wrap it to about 72
characters or so. In some contexts, the first line is treated as the
subject of the commit and the rest of the text as the body. The
blank line separating the summary from the body is critical (unless
you omit the body entirely); various tools like `log`, `shortlog`
and `rebase` can get confused if you run the two together.

Explain the problem that this commit is solving. Focus on why you
are making this change as opposed to how (the code explains that).
Are there side effects or other unintuitive consequences of this
change? Here's the place to explain them.

Further paragraphs come after blank lines.

* Bullet points are okay, too

* Typically a hyphen or asterisk is used for the bullet, preceded
  by a single space, with blank lines in between, but conventions
  vary here

Add references to the relevant issues in GitHub:

Fixes #123
See also #456, #789
```


## Pull Requests
We follow a handful of conventions when opening pull requests that enable the team to efficiently review code.

#### Pull Request Content
Strive to open pull requests that are large enough in scope to address the issue at hand but small enough for other team members to easily understand.

If you _are_ working on a larger feature, break your PRs up into smaller chunks of functionality. This will enable the rest of the team to more effectively wrap their heads around your proposed changes.

#### Pull Request Titles
Take care in the manner with which you title your pull requests. Use valid grammar and explain the intent of your proposed changes as concisely as possible.

#### Pull Request Body
Include the following items in your pull request body:

* **Notes:** Add any optional notes that may be helpful to the rest of the team. Stuff like: `Don't merge until x` or `This will not be merged into master, but into branch-x` - [ sample](https://github.guidebook.com/Guidebook/new-gears/pull/3218).
* **Why/Overview:** Add a section to explain the motivation for these changes. [sample](https://github.guidebook.com/Guidebook/new-gears/pull/2987) -
* **What:** Add a section to provide a high-level overview of the proposed changes. [sample](https://github.guidebook.com/Guidebook/new-gears/pull/3218) -
* **Testing Instructions:** If your feature needs to be QA'd, add reasonable testing instructions - [ sample](https://github.guidebook.com/Guidebook/new-gears/pull/3308).
* **References:** It is always helpful to add a link to the GitHub issue (as well as any other related issues) in your body for easy access.

#### Pull Request Labels
We use the following labels to indicate different status' to the rest of the team:

* **Ready For Review:** Your PR is ready to be reviewed by others.
* **DO NOT MERGE:** Your PR should *not* be merged (typically due to a blockage by a third party dependency, etc.)
* **Do Not Review:** Your PR is *not* ready to be reviewed by others. People still review these -- I would advise not opening a PR until its actually ready to be reviewed by others.
* **On Hold:** Indicates that the PR has been reviewed and the contributor is addressing feedback.
* **Schema Migration:** PR contains a schema migration. PLEASE USE THIS TAG IF YOUR PR CONTAINS A SCHEMA MIGRATION.
* **URGENT:** There is a time constraint around this pull request.


## Merging
In almost every case, another developer should merge or give you approval to merge your pull request into `main`. Only under the most pressing circumstances (ie: things are on fire!) should you merge your own changes before they have been reviewed.