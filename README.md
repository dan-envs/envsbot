# envsbot

> ⚠️ **Status: Early Development**
> This project is currently in an early development stage and may change
> significantly.
> Features, APIs, and internal structures are not yet considered stable.
>
> It's not nearly complete and very important parts (like user management) are
> still missing

## envs pubnix/tilde
**envsbot** is planned for use on the '**envs**' pubnix / tilde shared Linux
multiuser environment community.

---

**envsbot** is a modular, plugin-driven chat bot framework written in Python.

The project focuses on simplicity, clean architecture, and runtime extensibility.  
Features are implemented as plugins which can be dynamically loaded, unloaded,
or reloaded without restarting the bot.

envsbot is designed to make it easy to extend functionality while keeping the
core bot lightweight and maintainable.

---

## Features

* Plugin-based architecture
* Dynamic plugin loading / unloading / reload
* Command handling system
* Plugin dependency support
* Structured database layer
* Clean and modular codebase
* Extensive automated test suite

---

## Project Structure

~~~
envsbot/
│
├─ bot.py                    # Main bot runtime
│
├─ utils/                    # Core framework utilities
│   ├─ command.py            # Command registry and decorators
│   ├─ plugin_manager.py     # Plugin loading and lifecycle management
│   └─ config.py             # Configuration loader / helpers
│
├─ database/                 # Database modules
│   ├─ manager.py            # Database manager / connection handling
│   ├─ rooms.py              # Room storage logic
│   └─ users.py              # User storage logic
│
├─ plugins/                  # Bot plugins
│   ├─ help.py
│   ├─ plugins.py
│   ├─ rooms.py
│   ├─ status.py
│   ├─ _reg_profile.py       # Internal self registration/profile plugin (vCard)
│   └─ _test.py              # Development / testing plugin
│
├─ tests/                    # Automated test suite
│   ├─ conftest.py           # Global pytest fixtures
│   ├─ xmpp_fixtures.py
│   │
│   ├─ bot_core/             # Core bot behaviour tests
│   │   ├─ test_bot.py
│   │   ├─ test_permissions.py
│   │   └─ test_reply.py
│   │
│   ├─ commands/             # Command framework tests
│   │   ├─ test_commands.py
│   │   ├─ test_commands_crash.py
│   │   └─ test_commands_system.py
│   │
│   ├─ plugins/              # Plugin system tests
│   │   ├─ test_plugin_integrity.py
│   │   ├─ test_plugin_isolation.py
│   │   ├─ test_plugin_manager_property.py
│   │   ├─ test_plugin_manager_unit.py
│   │   ├─ test_plugin_reload.py
│   │   └─ test_plugin_reload_integrity.py
│   │
│   └─ integration/
│       └─ test_integration.py
│
├─ config_sample.json        # Example configuration
├─ requirements.txt
├─ requirements-dev.txt
├─ pyproject.toml
├─ LICENSE
└─ README.md
~~~

---

## Installation

Clone the repository:

~~~bash
git clone <repository-url>
cd envsbot
~~~

Create a virtual environment:

~~~bash
python3 -m venv venv
~~~

Activate the virtual environment:

**Linux / macOS**

~~~bash
source venv/bin/activate
~~~

**Windows**

~~~bash
venv\Scripts\activate
~~~

Install dependencies:

~~~bash
pip install -r requirements.txt
~~~

Create a configuration file:

~~~bash
cp config_sample.json config.json
~~~

Run the bot:

~~~bash
python bot.py
~~~

---

## Development

For development, install the additional development dependencies:

~~~bash
pip install -r requirements-dev.txt
~~~

These include tools required for running the automated test suite.

---

## Running Tests

The project includes an automated test suite.

Run all tests using:

~~~bash
pytest
~~~

---

## TODO

### Core framework improvements
* [ ] Improve safe hot-reload to prevent module memory leaks
* [ ] Move `PLUGIN_META` discovery into `plugin_manager`
* [ ] Improve plugin validation and error handling
* [ ] Add better debugging / inspection tools for the command registry

### Plugin system
* [ ] Add circular dependency detection for plugins
* [ ] Prevent unloading plugins that are required by other plugins
* [ ] Improve plugin dependency resolution
* [ ] Add plugin configuration support

### Core functionality still missing
* [ ] Implement proper user / permission management
* [ ] Expand bot configuration and persistence features
* [ ] Add more essential built-in plugins

### Development & tooling
* [ ] Expand automated test coverage
* [ ] Add documentation for plugin development
* [ ] Add CI pipeline (linting and tests)

---

## License

This project is licensed under the **MIT License**.
