<!-- omit in toc -->
# Regarding contributions

All types of contributions are encouraged and valued. See the [Table of contents](#table-of-contents) for different ways to help and details about how this project handles them. Please make sure to read the relevant section before making your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved. We look forward to your contributions.

<!-- omit in toc -->
## Table of contents

- [I want to contribute](#i-want-to-contribute)
  - [Reporting bugs](#reporting-bugs)
  - [Suggesting enhancements](#suggesting-enhancements)
  - [Code contribution](#code-contribution)

## I want to contribute

### Reporting bugs

#### Before submitting a bug report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible:

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions.
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker][issues_bugs].
- Also make sure to search the internet to see if users outside of the GitHub community have discussed the issue.
- Collect information about the bug:
  - Axis device model
  - Axis device firmware version
  - Stack trace
  - OS and version (Windows, Linux, macOS, x86, ARM)
  - Version of the interpreter, compiler, SDK, runtime environment, package manager, depending on what seems relevant
  - Possibly your input and the output
  - Can you reliably reproduce the issue? And can you also reproduce it with older versions?

#### How do I submit a good bug report?

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [issue][issues_new].
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the *reproduction steps* that someone else can follow to recreate the issue on their own.
- Provide the information you collected in the previous section.

Once it's filed:

- The project team will label the issue accordingly.
- A team member will try to reproduce the issue with your provided steps. If there are no reproduction steps or no obvious way to reproduce the issue, the team will ask you for those steps. Bugs without steps will not be addressed until they can be reproduced.
- If the team is able to reproduce the issue, it will be prioritized according to severity.

### Suggesting enhancements

This section guides you through submitting an enhancement suggestion, **including completely new features and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.

#### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Read the documentation carefully and find out if the functionality is already covered, maybe by an individual configuration.
- Perform a [search][issues] to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
- Find out whether your idea fits with the scope and aims of the project. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset.

#### How do I submit a good enhancement suggestion?

Enhancement suggestions are tracked as [GitHub issues][issues].

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point you can also tell which alternatives do not work for you.
- You may want to **include screenshots and animated GIFs** which help you demonstrate the steps or point out the part which the suggestion is related to.
- **Explain why this enhancement would be useful** to most users. You may also want to point out the other projects that solved it better and which could serve as inspiration.

### Code contribution

Start by [forking the repository](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo), i.e. copying the repository to your account to grant you write access. Continue with cloning the forked repository to your local machine.

```sh
git clone https://github.com/<your username>/axis-model-zoo.git
```

Navigate into the cloned directory and create a new branch:

```sh
cd axis-model-zoo
git switch -c <branch name>
```

Update the code according to your requirements, and commit the changes using the [conventional commits](https://www.conventionalcommits.org) message style:

```sh
git commit -a -m 'Follow the conventional commit messages style to write this message'
```

Continue with pushing the local commits to GitHub:

```sh
git push origin <branch name>
```

Before opening a Pull Request (PR), please consider the following guidelines:

- Please make sure that the sample code builds perfectly fine on your local system.
- Make sure that all linters pass.
- Follow the conventional commits message style in the commit messages
- The PR will have to meet the sample code examples standard already available in the repository.
- Explanatory comments related to code functions are required. Please write code comments for a better understanding of the code for other developers.
- No PR will be accepted without having a well defined README (see examples in the repo) file for the sample code.

And finally when you are satisfied with your changes, open a new PR.

#### Lint of code base

A set of different linters test the code base and these must pass in order to get a pull request approved. When you create a pull request, a set of linters will run syntax and format checks on different file types in GitHub Actions by making use of a tool called [super-linter](https://github.com/github/super-linter). If any of the linters gives an error, this will be shown in the action connected to the pull request.

In order to fasten up development, it's possible to run linters as part of your local development environment. Since super-linter is using a Docker image in GitHub Actions, users of other editors may run it locally to lint the code base. For complete instructions and guidance, see super-linter page for [running locally](https://github.com/github/super-linter/blob/main/docs/run-linter-locally.md).

To run a number of linters on the code base from command line:

```sh
docker run --rm  \
  -v $PWD:/tmp/lint \
  -e RUN_LOCAL=true \
  -e LINTER_RULES_PATH=/ \
  -e MARKDOWN_CONFIG_FILE=.markdownlint.yml \
  -e DOCKERFILE_HADOLINT_FILE_NAME=.hado-lint.yml \
  -e YAML_CONFIG_FILE=.yaml-lint.yml \
  -e VALIDATE_BASH=true \
  -e VALIDATE_DOCKERFILE_HADOLINT=true \
  -e VALIDATE_MARKDOWN=true \
  -e VALIDATE_SHELL_SHFMT=true \
  -e VALIDATE_YAML=true \
  github/super-linter:slim-v4
```

##### Run super-linter interactively

It might be more convenient to run super-linter interactively. Run container and enter command line:

```sh
docker run --rm \
  -v $PWD:/tmp/lint \
  -w /tmp/lint \
  --entrypoint /bin/bash \
  -it github/super-linter:slim-v4
```

Then from the container terminal, the following commands can lint the the code
base for different file types:

```sh
# Lint Dockerfile files
hadolint $(find -type f -name "Dockerfile*")

# Lint Markdown files
markdownlint .

# Lint YAML files
yamllint .

# Lint shell script files
shellcheck $(shfmt -f .)
shfmt -d .
```

To lint only a specific file, replace `.` or `$(COMMAND)` with the file path.

<!-- markdownlint-disable MD034 -->
[issues]: https://github.com/AxisCommunications/axis-model-zoo/issues
[issues_new]: https://github.com/AxisCommunications/axis-model-zoo/issues/new
[issues_bugs]: https://github.com/AxisCommunications/axis-model-zoo/issues?q=label%3Abug
<!-- markdownlint-enable MD034 -->
