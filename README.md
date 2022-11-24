
  

# multi-subject-render
Generate multiple complex subjects all at once!

Made as a script for the [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) repository.

![00157-1355719032-DDIM-64-7 5-579c005f-20221123190321](https://user-images.githubusercontent.com/15731540/203708003-9cbe7695-f512-4d7c-9cbb-54f8d6cb17f0.png)

<sub>_Kyaaaaaaaaaaaaaaaaa!_</sub>

[Jump to examples!](#a-few-more-examples)

## 💥 Installation 💥

- Run that command from the webui directory :

>git clone https://github.com/isl-org/MiDaS.git repositories/midas

Alternatively you can just copy the url of that repository into the extension tab :

![image](https://user-images.githubusercontent.com/15731540/203840132-cd8ce6a2-2843-4a96-8e35-b819af7bc01f.png)

OR copy that repository in your extension folder :

![image](https://user-images.githubusercontent.com/15731540/203840272-83cccb24-4417-44bc-99df-e45eb5f3360c.png)

You might need to restart the whole UI. Maybe twice.

## The look

![image](https://user-images.githubusercontent.com/15731540/203795296-3b917ab2-f0a3-4202-8b17-8d115b22bbe8.png)

<sub>OK I know that's a big screenshot </sub>

## How the hell does this works?

First it creates your background image, then your foreground subjects, then does a depth analysis on them, cut their backgrounds, paste them onto your background and then does an img2img for a smooth blend!


<sup>It will cut around that lady with scissors made of *code*.</sup>

![image](https://user-images.githubusercontent.com/15731540/203715689-791ff6d7-e1cd-4c86-99eb-7ecb2e60859a.png)


## Explanations of the different UI elements

### I will only explain the not so obvious things because I spent enough time making that thing already.

- First off, your usual UI will be for your initial background. So your normal prompt will probably be something like "a beach, sunny sky" etc.

For my example I decided to generate a bowling alley at 512x512 pixels :

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

## Tips and tricks :

- using (bokeh) and (F1.8:1.2) will make blurry backgrounds which will make it easier for the depth analysis to do a clean cut of the backgrounds.
- "wide angle" in your prompt will give your more chances to have characters that won't be cropped
- "skin details" or "detailed skin" raises the chances of having close-ups. I prefer to avoid.
- Not enough denoising/steps on your final blend will make it look like you used scissors on your moms Vogue catalogue and pasted the ladies onto your dads Lord of the Rings favorite poster. Don't do that.
- Too much denoising/steps might make the characters all look the same. It's all about finding the right middle value for your needs.
- Making your foreground subjects have less height than the final image might make them look cropped.

## Known issues

- It does only render the final blend to the UI. You have to save the images (like in the settings you just don't uncheck that "save all images" checkbox and you're good).
- There can be bugs.


## Credits

Thanks to [thygate](https://github.com/thygate) for letting me blatantly copy-paste some of his functions for the depth analysis.


## A few more examples

##### An attempt at recreating the ["Distracted boyfriend"](https://en.wikipedia.org/wiki/Distracted_boyfriend) meme. Without influencing the directions in which they are looking. 100% txt2img.

![00241-2439212203-Euler a-100-7 5-ac07d41f-20221124151538](https://user-images.githubusercontent.com/15731540/203824326-e3c02bb1-6318-4083-894d-4aa9e26903b2.png)
![00287-2439212203-Euler a-100-7 5-ac07d41f-20221124151832](https://user-images.githubusercontent.com/15731540/203824335-170d9620-2d7c-4538-a529-ac7b51ac718d.png)
![00123-60606195-DDIM-74-7 5-ac07d41f-20221124144302](https://user-images.githubusercontent.com/15731540/203824348-72f918cf-2df6-42ee-a9b6-69b7c9ff8309.png)
![00133-1894928239-DDIM-74-7 5-ac07d41f-20221124144525](https://user-images.githubusercontent.com/15731540/203824351-84e62d31-b1c5-4f41-8bfb-b7e2e0c4b287.png)

<sub> I messed up the order on the last one. </sub>

![00129-603508287-DDIM-64-7 5-ac07d41f-20221122153921](https://user-images.githubusercontent.com/15731540/203713258-aaeffbf7-5772-458d-804a-d09be35531fb.png)

<sub> Aren't they cute without oxygen? </sub>

![00051-3908280031-DPM++ 2M-74-7 5-ac07d41f-20221122145842](https://user-images.githubusercontent.com/15731540/203714620-e45dc7d6-ec26-4aee-b0e3-e1055d98c850.png)

<sub>Of course you can make a harem just for yourself.</sub>

![00165-603508287-DDIM-64-7 5-ac07d41f-20221122154627](https://user-images.githubusercontent.com/15731540/203716695-ab8d5764-0e68-414f-951e-29edac4cab5b.png)

<sub> MOAR KITTENS </sub>

Now a few more groups of "super heroes" from the same batch as the first image here. Except maybe for the portraits.

![00283-1347027508-DDIM-69-7 5-579c005f-20221123193425](https://user-images.githubusercontent.com/15731540/203719641-364dd072-4360-4afb-8a84-032cd5013f72.png)
![00238-2109887726-DDIM-69-7 5-579c005f-20221123192356](https://user-images.githubusercontent.com/15731540/203719659-4be6c008-eeca-4b53-b3e3-e8f31b933ba1.png)
![00349-3785266290-DDIM-76-7 5-579c005f-20221123194925](https://user-images.githubusercontent.com/15731540/203719670-03062253-e746-4b02-9517-f0576142e3c1.png)
![00290-1347027509-DDIM-69-7 5-579c005f-20221123193425](https://user-images.githubusercontent.com/15731540/203719705-15dfe420-1c08-4714-8892-632df4d9f3b4.png)

### Wrong settings examples

![00145-2998285171-DDIM-92-7 5-ac07d41f-20221124054225](https://user-images.githubusercontent.com/15731540/203716812-ea8a46b0-bbed-4f21-a5d3-10f231f3577c.png)

<sub> This is what too low denoising on the final blend looks like. Yuk!</sub>

![00254-1268283421-Euler a-68-7 5-ac07d41f-20221124060832](https://user-images.githubusercontent.com/15731540/203714476-c07a389d-25ee-48c7-9079-a95ff6c03248.png)

<sub> Same issue here. Looks like a funny kid collage. Grandma will love it because you typed your prompts with love and she knows it.</sub>


![affafasffasffasfas - Copie](https://user-images.githubusercontent.com/15731540/203717083-5938b8c5-2e20-45a0-9871-2558b7f7ff50.png)


<sub>Guess why I had to censor the lowest part. This is how too much denoising looks like. They look all the same.</sub>

