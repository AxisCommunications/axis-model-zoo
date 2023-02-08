# How to add new models to the auto-test framework

1. Copy the model in the [root models](../../models) directory
2. Create a hard symbolic link in the [application models](./larod-test/app/models) in the right subfolder. (to be improved)
3. Add a new row in the [README](../../README.md) adding a unique tag where the output of the test should be added.
4. Update the dictionary in [readme_update](./readme_update.py#L19) with the location of the new model, the camera model, and the tag where to place the results.
