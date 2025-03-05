from moviepy import *
from typing import Dict, Any

class TextClipFactory:
    """
    Factory class responsible for creating TextClip objects with validated parameters.
    """
    
    @staticmethod
    def create_text_clip(parameters: Dict[str, Any]) -> TextClip:
        """
        Creates and returns a TextClip object based on given parameters.

        :param parameters: Dictionary containing text clip properties.
        :return: Configured TextClip object.
        """
        TextClipFactory.validate_parameters(parameters)
        
        text_clip_params = {
            'text': parameters['text'],
            'font': parameters.get('font', 'Arial'),
            'color': parameters.get('color', 'white'),
            'stroke_width': parameters.get('stroke_width', 0),
            'stroke_color': parameters.get('stroke_color', 'black'),
            'size': parameters.get('size', (640, 480)),  # Default size
            'method': parameters.get('method', 'label'),
            'text_align': parameters.get('align', 'center')
        }
        
        if text_clip_params['method'] != 'caption':
            text_clip_params['font_size'] = parameters.get('fontsize', 24)

        text_clip = TextClip(**text_clip_params)

        # Apply start and end times if provided
        start_time = parameters.get('start_time', 0)
        end_time = parameters.get('end_time', None)
        
        text_clip = text_clip.set_start(start_time)
        if end_time is not None:
            text_clip = text_clip.set_duration(end_time - start_time)

        return text_clip
    
    @staticmethod
    def validate_parameters(parameters: Dict[str, Any]) -> None:
        """
        Validates that the required parameters exist and have appropriate values.

        :param parameters: Dictionary containing text clip properties.
        :raises ValueError: If required parameters are missing or invalid.
        """
        if 'text' not in parameters or not isinstance(parameters['text'], str) or not parameters['text'].strip():
            raise ValueError("The 'text' parameter is required and must be a non-empty string.")
        
        if 'fontsize' in parameters and (not isinstance(parameters['fontsize'], int) or parameters['fontsize'] <= 0):
            raise ValueError("The 'fontsize' parameter must be a positive integer.")
        
        if 'size' in parameters and (not isinstance(parameters['size'], tuple) or len(parameters['size']) != 2):
            raise ValueError("The 'size' parameter must be a tuple of two integers representing width and height.")
        
        if 'start_time' in parameters and (not isinstance(parameters['start_time'], (int, float)) or parameters['start_time'] < 0):
            raise ValueError("The 'start_time' parameter must be a non-negative number.")
        
        if 'end_time' in parameters:
            if (not isinstance(parameters['end_time'], (int, float)) or parameters['end_time'] <= parameters.get('start_time', 0)):
                raise ValueError("The 'end_time' parameter must be greater than 'start_time'.")
