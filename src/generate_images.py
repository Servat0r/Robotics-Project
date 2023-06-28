"""
Domain Randomization for Image Generation.
"""
import os
import random
from dotenv import load_dotenv
import numpy as np
import sys
from image_generation import cnn_generate_images
from datetime import datetime
import logging
logging.root.setLevel(logging.INFO)


def generate_randomized_dataset(n_iterations=10):
    motion_data_path = os.getenv('MOTION_DATA_PATH', 'data/motion/ws_0.5.npz')
    render_cmd = os.getenv('RENDER_CMD', None)
    if not render_cmd:
        raise ValueError(f'Render command not found')
    with open(os.getenv('LOG_FILE', 'dataset_generation_log.log'), 'w') as log_file:
        for i in range(n_iterations):
            os.makedirs(f'images/{i}', exist_ok=True)
            config = generate_random_configuration()
            logging.info(f"{i}-th configuration: '{config}'")
            print(f"[{datetime.now()}] {i}-th configuration: '{config}'", file=log_file, flush=True)
            cnn_generate_images(motion_data_path, config)
            os.system(render_cmd)
            os.system(f"powershell mv images/*.png images/{i}")
            logging.info(f'{i}-th image dataset generation completed')
            print(f"[{datetime.now()}] {i}-th image dataset generation completed", file=log_file, flush=True)


def generate_random_configuration():
    return {
        "rgb_terminals": list(np.random.randint(0, 255, 3, int)),
        "background_rgb": list(np.random.random(3)),
        "plane": random.choice(['monochromatic', 'checker', 'wood']),
        "monochromatic_rgb": list(np.random.random(3)),
        "wood_pigment": random.choice(['Cherry_Wood', 'Dark_Wood', 'Tan_Wood', 'White_Wood']),
        "spherical": False
    }


def main(env_file_path='.env'):
    load_dotenv(env_file_path)
    os.makedirs('images', exist_ok=True)
    os.makedirs('POV', exist_ok=True)
    num_iterations = int(os.getenv('NUM_ITERATIONS', 10))
    logging.info(f'Generating randomized dataset with {num_iterations} iterations ...')
    generate_randomized_dataset(num_iterations)
    logging.info('Dataset generation completed')


if __name__ == '__main__':
    env_file_path = sys.argv[1] if len(sys.argv) > 1 else '.env'
    main(env_file_path)
