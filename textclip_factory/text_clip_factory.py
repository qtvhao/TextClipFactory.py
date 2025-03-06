from moviepy import TextClip
from moviepy.video.fx import FadeIn, FadeOut, BlackAndWhite, MirrorX, MirrorY, Resize
from typing import Dict, Any, Callable

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
            'font': parameters.get('font', 'Roboto-Regular'),
            'color': parameters.get('color', 'white'),
            'stroke_width': parameters.get('stroke_width', 2),
            'stroke_color': parameters.get('stroke_color', 'black'),
            'size': parameters.get('size', (2560, 1440)),  # Default size
            'method': parameters.get('method', 'caption'),
            'horizontal_align': parameters.get('horizontal_align', 'center'),
            'text_align': parameters.get('align', 'center'),
            'interline': parameters.get('vertical_align', 5),
            'bg_color': parameters.get('bg_color', None),
            'margin': parameters.get('margin', (None, 10)),
            'font_size': parameters.get('fontsize', 48),
        }
        
        text_clip = TextClip(**text_clip_params)

        # Apply start and end times if provided
        start_time = parameters.get('start_time', 0)
        end_time = parameters.get('end_time', None)
        duration = parameters.get('duration', 5)  # Default duration to 5 seconds
        
        text_clip = text_clip.with_start(start_time)
        if end_time is not None:
            duration = end_time - start_time
        text_clip = text_clip.with_duration(duration)
        
        # Define effect mapping
        effect_mapping: Dict[str, Callable] = {
            'fadein': lambda clip, duration: FadeIn(min(duration, clip.duration if clip.duration else duration)).apply(clip),
            'fadeout': lambda clip, duration: FadeOut(min(duration, clip.duration if clip.duration else duration)).apply(clip) if clip.duration else clip,
            'blackwhite': lambda clip, _: BlackAndWhite().apply(clip),
            'mirrorx': lambda clip, _: MirrorX().apply(clip),
            'mirrory': lambda clip, _: MirrorY().apply(clip),
            'resize': lambda clip, scale: Resize(scale).apply(clip)
        }
        
        # Apply effects
        effects = parameters.get('effects', ["fadein,0.2", "fadeout,0.2"])
        
        for effect in effects:
            effect_name, *effect_value = effect.split(',')
            effect_value = float(effect_value[0]) if effect_value else None
            
            if effect_name in effect_mapping:
                if effect_name == 'fadeout' and text_clip.duration is None:
                    raise ValueError("Cannot apply 'fadeout' because the clip duration is not set.")
                text_clip = effect_mapping[effect_name](text_clip, effect_value if effect_value is not None else 0.5)
        
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
        
        if 'size' in parameters and (not isinstance(parameters['size'], tuple) or len(parameters['size']) != 2 or not all(isinstance(i, int) and i > 0 for i in parameters['size'])):
            raise ValueError("The 'size' parameter must be a tuple of two positive integers representing width and height.")
        
        if 'start_time' in parameters and (not isinstance(parameters['start_time'], (int, float)) or parameters['start_time'] < 0):
            raise ValueError("The 'start_time' parameter must be a non-negative number.")
        
        if 'end_time' in parameters:
            if (not isinstance(parameters['end_time'], (int, float)) or parameters['end_time'] <= parameters.get('start_time', 0)):
                raise ValueError("The 'end_time' parameter must be greater than 'start_time'.")
