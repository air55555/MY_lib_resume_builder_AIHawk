import os
from typing import Any
from string import Template
from typing import Any
from lib_resume_builder_AIHawk.resume import Resume
from lib_resume_builder_AIHawk.gpt_resume import LLMResumer
from lib_resume_builder_AIHawk.gpt_resume_job_description import LLMResumeJobDescription
import lib_resume_builder_AIHawk.utils as utils
from lib_resume_builder_AIHawk.module_loader import load_module
from lib_resume_builder_AIHawk.config import global_config

class ResumeGenerator:
    def __init__(self):
        pass
    
    def set_resume_object(self, resume_object):
         self.resume_object = resume_object

    def _create_resume(self, gpt_answerer: Any, style_path):
            gpt_answerer.set_resume(self.resume_object)
            template = Template(utils.html_template)
            message = template.substitute(markdown=gpt_answerer.generate_html_resume(), style_path=style_path)
            if os.path.exists(global_config.OUTPUT_FILE_PATH):
                os.remove(global_config.OUTPUT_FILE_PATH)
            with open(global_config.OUTPUT_FILE_PATH, 'x', encoding="utf-8") as output_file:
                output_file.write(message)
            print(f"The resume has been saved to {global_config.OUTPUT_FILE_PATH}")

    def create_resume(self, style_path):
        strings = load_module(global_config.STRINGS_MODULE_RESUME_PATH, global_config.STRINGS_MODULE_NAME)
        gpt_answerer = LLMResumer(global_config.API_KEY, strings)
        self._create_resume(gpt_answerer, style_path)

    def create_resume_job_description(self, style_path: str, url_job_description: str):
        strings = load_module(global_config.STRINGS_MODULE_RESUME_JOB_DESCRIPTION_PATH, global_config.STRINGS_MODULE_NAME)
        gpt_answerer = LLMResumeJobDescription(global_config.API_KEY, strings)
        gpt_answerer.set_job_description(url_job_description)
        self._create_resume(gpt_answerer, style_path)
