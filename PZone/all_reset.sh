echo "STOPING ALL SERVICES.."
sh stop_uwsgi.sh
echo "CLEAN ALL FILES AND LOGS.."
sh clean_files.sh
sh clean_logs.sh
echo "STARTING UWSGI SERVICES.."
sh start_uwsgi.sh
echo "START NGINX SERVICES.."
service nginx stop && service nginx start
echo "ALL RESET DONE!!"
echo "PLEASE OPEN http://localhost:80/initdb TO RE-INIT YOUR DATABASES TO COMPLETE THE PROCESS!!"
