# Run molecule locally

```shell
python3 -m venv .venv
source .venv/bin/activat
pip install ansible molecule molecule-plugins[docker] docker yamllint
mkdir -p molecule/default/roles
rsync -aP --delete --delete-excluded --exclude=.idea/ --exclude=.venv/ --exclude=.git/ --exclude=molecule/ ./ molecule/default/roles/reimarstier.jetbrains_installer
molecule test
yamllint .
```
