# INSTALL PREQS
yum install centos-release-scl
yum install rh-python36
yum install git
yum update -y nss curl libcurl

# INSTALL PYTHON MODULES
scl enable rh-python36 bash
pip install tornado
pip install requests
pip install beautifulsoup4
pip install tldextract
pip install pysocks

# DOWNLOAD CODE
adduser inovotna
cd /home/inovotna
git clone https://github.com/agajdosi/truednes.git
