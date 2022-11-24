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

## Explanations of the different UI elements

### I will only explain the not so obvious things because I spent enough time making that thing already.

- First off, your usual UI will be for your initial background. So your normal prompt will probably be something like "a beach, sunny sky" etc.

For my example I decided to generate a bowling alley at 512x512 pixels :

![00158-2629831387-Euler a-22-7 5-ac07d41f-1233221312123132](https://user-images.githubusercontent.com/15731540/203710944-cf2e2290-0374-427e-9415-36a3bc248530.png)

- Your foreground subjects will be described in that text box. You case use wildcards. If you only use the first line, that line will be used for every foreground subject that will be generated. If you use multiple lines, each line will be used for each foreground subject.

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

![image](https://user-images.githubusercontent.com/15731540/203711743-957edd16-0ed3-49a2-b643-068f1e541d89.png)

