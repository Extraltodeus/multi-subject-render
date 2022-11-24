Made as a script for the [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) repository.
# waifu-harem-diffusion
Generate entire harems of waifus using stable diffusion easily! 

![00157-1355719032-DDIM-64-7 5-579c005f-20221123190321](https://user-images.githubusercontent.com/15731540/203708003-9cbe7695-f512-4d7c-9cbb-54f8d6cb17f0.png)

<sub>_Kyaaaaaaaaaaaaaaaaa!_</sub>


## The look

![image](https://user-images.githubusercontent.com/15731540/203705906-15913db0-96af-4f35-97e5-ce33cc04b6ea.png)

<sub>OK I know that's a big screenshot </sub>

## How the hell does this works?

First it creates your background image, then your foreground subjects, then does a depth analysis on them, cut their backgrounds, paste them onto your background and then does an img2img for a smooth blend!

<sup>It will cut around that lady with scissors made of code</sup>
![image](https://user-images.githubusercontent.com/15731540/203715689-791ff6d7-e1cd-4c86-99eb-7ecb2e60859a.png)


## Explanations of the different UI elements

### I will only explain the not so obvious things because I spent enough time making that thing already.

- First off, your usual UI will be for your initial background. So your normal prompt will probably be something like "a beach, sunny sky" etc.

For my example I decided to generate a bowling alley at 512x512 pixels :

<sup> I used the main prompt text box in the main UI to do that. Just wrote "a bowling alley". </sup>
![00158-2629831387-Euler a-22-7 5-ac07d41f-1233221312123132](https://user-images.githubusercontent.com/15731540/203710944-cf2e2290-0374-427e-9415-36a3bc248530.png)



- Your foreground subjects will be described in that text box.
- You case use wildcards.
- If you only use the first line, that line will be used for every foreground subject that will be generated.
- If you use multiple lines, each line will be used for each foreground subject.

![image](https://user-images.githubusercontent.com/15731540/203708718-9a80f197-5d52-41b2-a98d-12cf006a6c2a.png)

<sub> Note : if you do that, you will need as many lines as foreground images generated. </sub>

For my example I made tree penguins :

![sdffsdsdfsdffsddsfsfd](https://user-images.githubusercontent.com/15731540/203710767-601458a8-1658-4464-a804-1b3f7f396348.png)



- That's how much the seed will be incremented at each image. If you set it to 0 you will get the same foregrounds every time. Probably not what you want unless you use the Extra option in your main UI and "Variation strength".

![image](https://user-images.githubusercontent.com/15731540/203709475-be80e2d8-16bb-4f51-9790-40861bdbd5b1.png)

- You can use a different sampler for the foregrounds. As well as a different CLIP value.

![image](https://user-images.githubusercontent.com/15731540/203709940-7c789b25-d403-4c58-8b2c-e2341491b79a.png)

- The final blend is there to either make a smooth pass over your collage or to make something more complex / add details to your combination.
- You can use different settings and samplers for your final blend. Make as you wish. The CLIP value will be the one you've set in your settings tab. Not the one for the foregrounds. So you can decide if you prefer one way or the other. 

![00162-2629838387-Euler a-92-7 5-ac07d41f-20221124054727](https://user-images.githubusercontent.com/15731540/203711140-ccb3d22e-8687-45e4-a339-12d72f1915a2.png)

<sub> The are not really playing bowling because you need fingers. They're just here for trouble. </sub>

- An important part is to set the final blend width. Your initial background will be stretched to that size so you don't really need to make it initially big. Your foregrounds subjects will be pasted onto your stretched background before the final blend. Not wide enough and you will end up having too many characters at the same spot.

![image](https://user-images.githubusercontent.com/15731540/203711440-c8330086-cd1a-48be-8bf5-4eeacc1d5396.png)

#### The scary miscellaneous options :

- The foreground distance from center multiplier will make your characters closer together if you select a lower value, further with a higher one. I usually stick in between 0.8 and 1.0

- Foreground Y shift : the center character will always be at the same height. The you multiply the value of that slider by the position of the foreground subject from the center. That gives you how many pixels lower they will be. Think about some super hero movie poster with the sidies slightly lower. That's what this slider does.

- Foreground depth cut treshold is the scary one. At 0 the backgrounds of your foregrounds subjects will be opaque. At 255 the entire foreground will be transparent. The best values are in between 50-60 for cartoon-like characters and 90-100 for photorealistic subjects. Too much and they lose their heads, not enough and you get some rock that were sitting on in your final blend.

- Random superposition : the default is to have the center character in front. if you enable that it might not be the case anymore. That's a cool option depending on what you want to do.

- The center character will be behind the others. If you use the previous option this one becomes useless.

- face correction is only for the final blend. If you want that on every foreground subjects, set it in your main UI. It think it's best to enable both if you make photorealistic stuff.

![image](https://user-images.githubusercontent.com/15731540/203711743-957edd16-0ed3-49a2-b643-068f1e541d89.png)

### Tips and tricks :

- using (bokeh) and (F1.8:1.2) will make blurry backgrounds which will make it easier for the depth analysis to do a clean cut of the backgrounds.
- "wide angle" in your prompt will give your more chances to have characters that won't be cropped
- "skin details" or "detailed skin" raises the chances of having close-ups. I prefer to avoid.
- Not enough denoising/steps on your final blend will make it look like you used scissors on your moms Vogue catalogue and pasted the ladies onto your dads Lord of the Rings favorite poster. Don't do that.
- Too much denoising/steps might make the characters all look the same. It's all about finding the right middle value for your needs.


A few more examples :

![00129-603508287-DDIM-64-7 5-ac07d41f-20221122153921](https://user-images.githubusercontent.com/15731540/203713258-aaeffbf7-5772-458d-804a-d09be35531fb.png)

<sub> Aren't they cute without oxygen? </sub>


![00254-1268283421-Euler a-68-7 5-ac07d41f-20221124060832](https://user-images.githubusercontent.com/15731540/203714476-c07a389d-25ee-48c7-9079-a95ff6c03248.png)

<sub> You can also make absolute non-sens like Jesus, a t-rex and santa.</sub>



![00051-3908280031-DPM++ 2M-74-7 5-ac07d41f-20221122145842](https://user-images.githubusercontent.com/15731540/203714620-e45dc7d6-ec26-4aee-b0e3-e1055d98c850.png)

<sub>Of course you can make a harem just for yourself.</sub>



![00258-4071542780-Euler a-70-7-579c005f-20221123231254](https://user-images.githubusercontent.com/15731540/203715010-216c5a8d-4f87-414a-8b85-c544349a556b.png)

<sub> A nasty case of yoghurt addiction for sure. </sub>


<sub></sub>

