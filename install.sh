pip install -r requirements.txt
cp sr1168c-json.service /etc/systemd/system/.
systemctl enable sr1168c-json.service
systemctl start sr1168c-json.service
