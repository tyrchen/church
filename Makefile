CHECK=\033[32m✔\033[39m
DONE="\n$(CHECK) Done.\n"

SERVER=jcnrd.us
PROJECT=church
PATH=deployment/$(PROJECT)
SUPERVISORCTL=/usr/bin/supervisorctl
SUCOPY=/bin/sucopy
SSH=/usr/bin/ssh
ECHO=/bin/echo -e
NPM=/usr/local/bin/npm
PIP=/usr/bin/pip
SUDO=/usr/bin/sudo

remote_deploy:
	@$(SSH) -t $(SERVER) "echo Deploy $(PROJECT) to the $(SERVER) server.; cd $(PATH); git pull; make deploy;"

dependency:
	@$(ECHO) "\nInstall project dependencies..."
	@$(PIP) install -r requirements.txt

configuration:
	@$(ECHO) "\nUpdate configuration..."
	@$(SUDO) $(SUCOPY) -r _deploy/etc/. /etc/.

supervisor:
	@$(ECHO) "\nUpdate supervisor configuration..."
	@$(SUDO) $(SUPERVISORCTL) reread
	@$(SUDO) $(SUPERVISORCTL) update
	@$(ECHO) "\nRestart $(PROJECT)..."
	@$(SUDO) $(SUPERVISORCTL) restart $(PROJECT)

nginx:
	@$(ECHO) "\nRestart nginx..."
	@$(SUDO) /etc/init.d/nginx restart

deploy: dependency configuration supervisor nginx
	@$(ECHO) $(DONE)
