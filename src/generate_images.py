"""
Domain Randomization for Image Generation.
"""
import os
import json
from dotenv import load_dotenv
import numpy as np
import sys
from image_generation import cnn_generate_images


def main(env_file_path='.env'):
    load_dotenv(env_file_path)
    print(os.getenv('PIPPO', 'inia'))
    print(os.getenv('JSON_CONFIG', 'alala'))
    os.system('mkdir images')
    os.system('mkdir POV')
    json_config = json.load(open(os.getenv('JSON_CONFIG', 'src/config.json'), 'r'))
    motion_data_path = os.getenv('MOTION_DATA_PATH', 'data/motion/ws_0.5.npz')
    cnn_generate_images(motion_data_path, json_config)
    os.system(os.getenv('RENDER_CMD', 'echo Render command not found'))
    print('Completed')


if __name__ == '__main__':
    env_file_path = sys.argv[1] if len(sys.argv) > 1 else '.env'
    main(env_file_path)
