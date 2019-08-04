# Install Jetbrains Ansible Role
This ansible role is able to install a list of Jetbrains Tools.
* The latest version of the respective tool will be fetched from the jetbrains data services.
* Tools will be installed to `/opt`.
* Old versions will be automatically removed by default.
Simply put the name of the tool (as defined in the update URLs) in the `jetbrains_installer` list.
See example playbook below.

## Example Playbook
```
#!/usr/bin/env ansible-playbook
---
- hosts: host
  become: true
  gather_facts: True
  vars:
    username: 'me'
    jetbrains_installer:
    - name: "IntelliJ IDEA Community"
    - name: "PyCharm Community"
    - name: "Webstorm"
    - name: "RubyMine"
    - name: "GoLand"
    jetbrains_installer_bin_dir: "/opt/bin"
    jetbrains_installer_dir: "/opt"
    jetbrains_installer_remove_old_tools: True

  roles:
    - {role: 'jetbrains_installer', tags: ['jetbrains']}


```

## Update URLs
Jetbrains publishes their latest release version ids on following addresses:
* https://data.services.jetbrains.com/products/releases?code=TBA%2CIIU%2CPCP%2CWS%2CPS%2CRS%2CRD%2CCL%2CDG%2CRM%2CAC%2CGO%2CRC%2CDPK%2CDP%2CDM%2CDC%2CYTD%2CTC%2CUS%2CHB%2CMPS%2CPCE&latest=true&type=release&build=&_=1558842615517
* https://www.jetbrains.com/updates/updates.xml
* https://data.services.jetbrains.com/products/releases?code=PCP&latest=true&type=release&build=
* https://data.services.jetbrains.com/products/releases?code=IIC&latest=true&type=release&build=
