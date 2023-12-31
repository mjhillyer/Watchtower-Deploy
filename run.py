import argparse
import os
import importlib
from utils.deployment import Deployment, UnDeploy, Initialize
from utils.prompts import Prompt, Colors


def get_deployment_type(deployment_type_list):
    Prompt.question_banner("Deployment Choices:", True)
    Prompt.banner(deployment_type_list, prevent_all_option=True)
    return deployment_type_list[Prompt.get_response("Choice: ", deployment_type_list) - 1]


def run(options):
    path = f"deployments.{options['type']}.{options['action']}"
    validator_config = os.path.join(f"{os.path.sep}".join(path.split('.')[:-1]), 'config-validator.json')
    importlib.import_module(path)

    if options['action'] == 'init':
        init_classes = Initialize.__subclasses__()
        if not init_classes:
            Prompt.error(f"Unable to find class inheriting `Initialize` in {path}", close=True)
        if not os.path.exists(validator_config):
            Prompt.error(
                f"File does not exist: {validator_config}.  Each deployment type must have this file to validate required values for deployment.",
                close=True)
        init = init_classes[0](validator_config, options)
        init.generate()
        return

    Prompt.warning(f"Attempting to [{options['action']}] using the [{options['type']}] method")
    if options['action'] == 'deploy':
        if not options['config']:
            Prompt.error(f"Deployments require a configuration json that satisfies: [{validator_config}].  Please run: {Colors.CYAN}python run.py init", close=True)
        deployment_classes = Deployment.__subclasses__()
        if not deployment_classes:
            Prompt.error(f"Unable to find class inheriting `Deployment` in {path}", close=True)
        if not os.path.exists(validator_config):
            Prompt.error(
                f"File does not exist: {validator_config}.  Each deployment type must have this file to validate required values for deployment.",
                close=True)
        deployment = deployment_classes[0](options, validator_config)
        deployment.validate()
        os.chdir(f"deployments/{options['type']}")
        try:
            deployment.run()
        finally:
            deployment.cleanup()
        deployment.on_complete()
        Prompt.success(f"Deployment complete - using the [{options['type']}] method")
    else:
        deployment_classes = UnDeploy.__subclasses__()
        if not deployment_classes:
            Prompt.error(f"Unable to find class inheriting `UnDeploy` in {path}", close=True)
        remove_deployment = deployment_classes[0](options)
        os.chdir(f"deployments/{options['type']}")
        try:
            remove_deployment.run()
        finally:
            remove_deployment.cleanup()

        remove_deployment.on_complete()
        Prompt.success(f"Deployment removed - using the [{options['type']}] method")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deploy/Undeploy Watchtower:Flow')
    parser.add_argument('action', help='The action to take (init, deploy, undeploy)')
    parser.add_argument('--config', help='Config file - used to deploy process', required=False)
    parser.add_argument('--type', help="(Optional) Deployment type; It will prompt you if you don't include.",
                        required=False)

    args, unknown = parser.parse_known_args()
    args = vars(args)
    args['extra'] = unknown

    valid_actions = ['deploy', 'undeploy', 'init']
    if args['action'] not in valid_actions:
        Prompt.error(f"{args['action']} is not a valid choice.  Choices: {valid_actions}", close=True)

    deployment_types = sorted([y for y in [x[0].split(os.path.sep)[-1] for x in os.walk('deployments')][1:] if
                               not y.startswith('__')])
    if not args['type']:
        args['type'] = get_deployment_type(deployment_types)
    if args['type'] not in deployment_types:
        Prompt.error(f"{args['type']} is not a valid choice.  Choices: {deployment_types}", close=True)

    run(args)
