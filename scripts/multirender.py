from modules.processing import Processed, StableDiffusionProcessingImg2Img, process_images, images, fix_seed
from modules.shared import opts, cmd_opts, state
from PIL import Image, ImageOps, ImageFilter
from math import ceil
import cv2

import modules.scripts as scripts
from modules import sd_samplers
from random import randint, shuffle
import random
from skimage.util import random_noise
import gradio as gr
import numpy as np
import sys
import os
import importlib.util

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class Script(scripts.Script):
    def title(self):
        return "Multi Subject Rendering"

    def show(self, is_img2img):
        return not is_img2img

    def ui(self, is_img2img):
        if is_img2img: return
        txt2img_samplers_names = [s.name for s in sd_samplers.samplers]
        img2img_samplers_names = [s.name for s in sd_samplers.samplers_for_img2img]
        midas_models = ["midas_v21_small","dpt_swin2_tiny_256","dpt_swin2_large_384","dpt_beit_large_512"]
        
        #pick model
        with gr.Box():
            with gr.Box():
                gr.Markdown(
                """
                #### ATTENTION! Largest model (dpt_beit_large_512) weighs 1.5 GB, it will take A WHILE to download.

                """)
            foregen_midas_model = gr.Dropdown(label="MiDaS model (models are ordered from smallest and least accurate (midas_v21_small) to biggest and most accurate (dpt_beit_large_512))", choices=midas_models, value="midas_v21_small")
        
        # foreground UI
        with gr.Box():
            foregen_prompt      = gr.Textbox(label="Foreground prompt  ", lines=5, max_lines=2000)
            foregen_iter        = gr.Slider(minimum=1, maximum=10, step=1, label='Number of foreground images  ', value=5)
            foregen_steps       = gr.Slider(minimum=1, maximum=120, step=1, label='foreground steps  ', value=24)
            foregen_cfg_scale   = gr.Slider(minimum=1, maximum=30, step=0.1, label='foreground cfg scale  ', value=12.5)
            foregen_seed_shift  = gr.Slider(minimum=0, maximum=1000, step=1, label='foreground new seed+  ', value=1000)
            foregen_sampler     = gr.Dropdown(label="foreground sampler", choices=txt2img_samplers_names, value="DDIM")
            foregen_clip        = gr.Slider(minimum=0, maximum=12, step=1, label='change clip for foreground (0 = no interaction)  ', value=0)
            with gr.Row():
                foregen_size_x  = gr.Slider(minimum=64, maximum=2048, step=64, label='foreground width (64 = same as background)  ', value=64)
                foregen_size_y  = gr.Slider(minimum=64, maximum=2048, step=64, label='foreground height (64 = same as background)  ', value=64)

        # blend UI
        with gr.Box():
            foregen_blend_prompt             = gr.Textbox(label="final blend prompt", lines=2, max_lines=2000)
            foregen_blend_steps              = gr.Slider(minimum=1, maximum=120, step=1, label='blend steps   ', value=64)
            foregen_blend_cfg_scale          = gr.Slider(minimum=1, maximum=30, step=0.1, label='blend cfg scale  ', value=7.5)
            foregen_blend_denoising_strength = gr.Slider(minimum=0.1, maximum=1, step=0.01, label='blend denoising strength   ', value=0.42)
            foregen_blend_sampler            = gr.Dropdown(label="blend sampler", choices=img2img_samplers_names, value="DDIM")
            with gr.Row():
                foregen_blend_size_x  = gr.Slider(minimum=64, maximum=2048, step=64, label='blend width   (64 = same size as background) ', value=64)
                foregen_blend_size_y  = gr.Slider(minimum=64, maximum=2048, step=64, label='blend height  (64 = same size as background) ', value=64)

        # Misc options
        foregen_x_shift  = gr.Slider(minimum=0, maximum=2, step=0.01, label='Foreground distance from center multiplier  ', value=1)
        foregen_y_shift  = gr.Slider(minimum=0, maximum=100, step=1, label='Foreground Y shift (far from center = lower) ', value=0)
        foregen_treshold = gr.Slider(minimum=0, maximum=255, step=1, label='Foreground depth cut threshold', value=92)
        with gr.Row():
            foregen_save_background = gr.Checkbox(label='Save background ', value=True)
            foregen_save_all        = gr.Checkbox(label='Save all foreground images ', value=True)
            foregen_face_correction = gr.Checkbox(label='Face correction ', value=True)
            foregen_random_superposition = gr.Checkbox(label='Random superposition ', value=False)
            foregen_reverse_order = gr.Checkbox(label='Reverse order ', value=False)
            foregen_make_mask = gr.Checkbox(label='Mask foregrounds in blend', value=False)
        # foregen_mask_blur = gr.Slider(minimum=0, maximum=12, step=1, label='Mask blur', value=4)
        return    [foregen_prompt,
                    foregen_iter,
                    foregen_steps,
                    foregen_cfg_scale,
                    foregen_seed_shift,
                    foregen_sampler,
                    foregen_clip,
                    foregen_size_x,
                    foregen_size_y,
                    foregen_blend_prompt,
                    foregen_blend_steps,
                    foregen_blend_cfg_scale,
                    foregen_blend_denoising_strength,
                    foregen_blend_sampler,
                    foregen_blend_size_x,
                    foregen_blend_size_y,
                    foregen_x_shift,
                    foregen_y_shift,
                    foregen_treshold,
                    foregen_save_background,
                    foregen_save_all,
                    foregen_face_correction,
                    foregen_random_superposition,
                    foregen_reverse_order,
                    foregen_make_mask,
                    foregen_midas_model
                    ]




    def run(self,p,foregen_prompt,
                    foregen_iter,
                    foregen_steps,
                    foregen_cfg_scale,
                    foregen_seed_shift,
                    foregen_sampler,
                    foregen_clip,
                    foregen_size_x,
                    foregen_size_y,
                    foregen_blend_prompt,
                    foregen_blend_steps,
                    foregen_blend_cfg_scale,
                    foregen_blend_denoising_strength,
                    foregen_blend_sampler,
                    foregen_blend_size_x,
                    foregen_blend_size_y,
                    foregen_x_shift,
                    foregen_y_shift,
                    foregen_treshold,
                    foregen_save_background,
                    foregen_save_all,
                    foregen_face_correction,
                    foregen_random_superposition,
                    foregen_reverse_order,
                    foregen_make_mask,
                    foregen_midas_model
                    ):
        initial_CLIP = opts.data["CLIP_stop_at_last_layers"]
        sdmg = module_from_file("simple_depthmap",'extensions/multi-subject-render/scripts/simple_depthmap.py')
        sdmg = sdmg.SimpleDepthMapGenerator(foregen_midas_model) #import midas

        def cut_depth_mask(img,mask_img,foregen_treshold):
            img = img.convert("RGBA")
            mask_img = mask_img.convert("RGBA")
            mask_datas = mask_img.getdata()
            datas = img.getdata()
            treshold = foregen_treshold
            newData = []
            for i in range(len(mask_datas)):
                if mask_datas[i][0] >= foregen_treshold and mask_datas[i][1] >= foregen_treshold and mask_datas[i][2] >= foregen_treshold:
                    newData.append(datas[i])
                else:
                    newData.append((255, 255, 255, 0))
            mask_img.putdata(newData)
            return mask_img

        def paste_foreground(background,foreground,index,total_foreground,x_shift,y_shift,foregen_reverse_order):
            background = background.convert("RGBA")
            if not foregen_reverse_order:
                index = total_foreground-index-1
            image = Image.new("RGBA", background.size)
            image.paste(background, (0,0), background)
            alternator = -1 if index % 2 == 0 else 1
            if total_foreground % 2 == 0:
                foreground_shift  = background.size[0]/2-foreground.size[0]/2 + background.size[0]/(total_foreground)*alternator*ceil(index/2)*x_shift - background.size[0]/(total_foreground)/2
            else:
                index_shift = index-(index % 2)
                if index == 0:
                    foreground_shift  = background.size[0]/2-foreground.size[0]/2
                else:
                    foreground_shift  = background.size[0]/2-foreground.size[0]/2 + background.size[0]/(total_foreground)*alternator*ceil(index/2)*x_shift
            x_shift = int(foreground_shift)
            y_shift = ceil(index/2)*y_shift
            image.paste(foreground, (x_shift,background.size[1]-foreground.size[1]+y_shift), foreground)
            return image

        fix_seed(p)
        p.do_not_save_samples = not foregen_save_background

        foregen_size_x = p.width  if foregen_size_x == 64 else foregen_size_x
        foregen_size_y = p.height if foregen_size_y == 64 else foregen_size_y
        foregen_blend_size_x = p.width  if foregen_blend_size_x == 64 else foregen_blend_size_x
        foregen_blend_size_y = p.height if foregen_blend_size_y == 64 else foregen_blend_size_y

        o_sampler_name = p.sampler_name
        o_prompt    = p.prompt
        o_cfg_scale = p.cfg_scale
        o_steps     = p.steps
        o_do_not_save_samples = p.do_not_save_samples
        o_width     = p.width
        o_height    = p.height
        o_denoising_strength = p.denoising_strength


        n_iter=p.n_iter
        for j in range(n_iter):
            if state.interrupted:
                if foregen_clip > 0:
                    opts.data["CLIP_stop_at_last_layers"] = initial_CLIP
                break
            p.n_iter=1

            #background image processing
            if foregen_clip > 0:
                opts.data["CLIP_stop_at_last_layers"] = initial_CLIP
            p.prompt = o_prompt
            p.sampler_name = o_sampler_name
            p.cfg_scale = o_cfg_scale
            p.steps = o_steps
            p.do_not_save_samples = o_do_not_save_samples
            p.width = o_width
            p.height = o_height
            p.denoising_strength = o_denoising_strength

            proc = process_images(p)
            background_image = proc.images[0]

            # foregrounds processing
            foregen_prompts = foregen_prompt.splitlines()
            foregrounds = []
            if foregen_clip > 0:
                opts.data["CLIP_stop_at_last_layers"] = foregen_clip
            for i in range(foregen_iter):
                if state.interrupted:
                    if foregen_clip > 0:
                        opts.data["CLIP_stop_at_last_layers"] = initial_CLIP
                    break
                p.prompt    = foregen_prompts[i] if len(foregen_prompts) > 1 else foregen_prompt
                p.seed      = p.seed + foregen_seed_shift
                p.subseed   = p.subseed + 1 if p.subseed_strength > 0 else p.subseed
                p.cfg_scale = foregen_cfg_scale
                p.steps     = foregen_steps
                p.do_not_save_samples = not foregen_save_all
                p.sampler_name = foregen_sampler
                p.width     = foregen_size_x
                p.height    = foregen_size_y
                p.denoising_strength  = None

                proc = process_images(p)
                foregrounds.append(proc.images[0])

            # put back clip to original settings before img2img final blend
            if foregen_clip > 0:
                opts.data["CLIP_stop_at_last_layers"] = initial_CLIP

            #stretch background to final blend if the final blend as a specific size set
            if o_width != foregen_blend_size_x or o_height != foregen_blend_size_y :
                background_image = background_image.resize((foregen_blend_size_x, foregen_blend_size_y), Image.Resampling.LANCZOS)

            image_mask_background = Image.new(mode = "RGBA", size = (foregen_blend_size_x, foregen_blend_size_y), color = (0, 0, 0, 255))
            # cut depthmaps and stick foreground on the background
            random.seed(p.seed)
            random_order = [k for k in range(foregen_iter)]
            if foregen_random_superposition :
                shuffle(random_order)

            for f in range(foregen_iter):
                foreground_image      = foregrounds[f]
                # gen depth map
                foreground_image_mask = sdmg.calculate_depth_map_for_waifus(foreground_image)
                # cut depth
                foreground_image      = cut_depth_mask(foreground_image,foreground_image_mask,foregen_treshold)
                # paste foregrounds onto background
                background_image      = paste_foreground(background_image,foreground_image,random_order[f],foregen_iter,foregen_x_shift,foregen_y_shift,foregen_reverse_order)
                #make mask
                if foregen_make_mask:
                    foreground_image_mask      = cut_depth_mask(foreground_image_mask,foreground_image_mask,foregen_treshold)
                    image_mask_background = paste_foreground(image_mask_background,foreground_image_mask,random_order[f],foregen_iter,foregen_x_shift,foregen_y_shift,foregen_reverse_order)

            if foregen_make_mask:
                image_mask_p = image_mask_background
                # if foregen_mask_blur > 0:
                #     image_mask_p = image_mask_p.filter(ImageFilter.GaussianBlur(foregen_mask_blur)) # for some reason mask blur did not seem to work so I make it here.
            else:
                image_mask_p = None
            # final blend
            img2img_processing = StableDiffusionProcessingImg2Img(
                init_images=[background_image],
                resize_mode=0,
                denoising_strength=foregen_blend_denoising_strength,
                mask=image_mask_p,
                mask_blur=0,
                inpainting_fill=1,
                inpaint_full_res=True,
                inpaint_full_res_padding=0,
                inpainting_mask_invert=1,
                sd_model=p.sd_model,
                outpath_samples=p.outpath_samples,
                outpath_grids=p.outpath_grids,
                prompt=foregen_blend_prompt,
                styles=p.styles,
                seed=p.seed+foregen_seed_shift*(foregen_iter+1),
                subseed=p.subseed,
                subseed_strength=p.subseed_strength,
                seed_resize_from_h=p.seed_resize_from_h,
                seed_resize_from_w=p.seed_resize_from_w,
                sampler_name=foregen_blend_sampler,
                batch_size=p.batch_size,
                n_iter=p.n_iter,
                steps=foregen_blend_steps,
                cfg_scale=foregen_blend_cfg_scale,
                width=foregen_blend_size_x,
                height=foregen_blend_size_y,
                restore_faces=foregen_face_correction,
                tiling=p.tiling,
                do_not_save_samples=False,
                do_not_save_grid=p.do_not_save_grid,
                extra_generation_params=p.extra_generation_params,
                overlay_images=p.overlay_images,
                negative_prompt=p.negative_prompt,
                eta=p.eta
                )
            final_blend = process_images(img2img_processing)
            p.subseed = p.subseed + 1 if p.subseed_strength  > 0 else p.subseed
            p.seed    = p.seed    + 1 if p.subseed_strength == 0 else p.seed
        return final_blend
