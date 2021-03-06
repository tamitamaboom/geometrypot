import os
import discord
import random
from discord.ext import commands
from discord.ext import tasks

bot = commands.Bot(command_prefix='?>') #กำหนด Prefix
@bot.event
async def on_ready() : #เมื่อระบบพร้อมใช้งาน
    print("Bot Started!") #แสดงผลใน CMD
@bot.event
async def on_message(message) : #ดักรอข้อความใน Chat
    if message.content.startswith('?>ping') : #เมื่อข้อความในตัวแรกมีคำว่า ping
       await message.channel.send('Pong ~ Meow ><') #ข้อความที่ต้องการตอบกลับ
    await bot.process_commands(message)

@bot.command(pass_context = True , aliases=['สถานะ'])
async def status(ctx, pot) :
    import requests
    import json
    print(pot)
    await ctx.send("กำลังหาข้อมูลสถานะกระถางที่ "+str(pot))
    x = requests.get("http://localhost:5555/status/"+str(pot)+"/all")
    print(x.json())
    if x.json()["light"] == 0:
        l = "ไฟปิดอยู่"
    else:
        l = "ไฟเปิดอยู่"
    if x.json()["tank"] == 0:
        h = "ใกล้หมด"
    else:
        h = "ปกติ"
    await ctx.send(
        "ไฟ: "+l 
        +"\nความชื้น: "+ str(x.json()["humid"]) + "%"
        +"\nอุณหภูมิ: "+ str(x.json()["temp"]) + "องศาเซลเซียส"
        +"\nน้ำในถัง: "+ h
    )

@bot.command(pass_context = True , aliases=['ตั้งค่า'])
async def setting(ctx, mode, pot, data) :
    import requests
    import json
    mode_dict = {
        "เวลาเปิดไฟ":"light",
        "ความชื้น":"humid",
        "อุณหภูมิ":"temp"
    }
    print(data)
    print(type(data))
    if mode_dict[str(mode)] == "light":
        data = data.split("-")
        for i in range(len(data)):
            data[i] = float(data[i])
    else:
        data = int(data)
    obj = {"data": data}
    print(pot)
    await ctx.send("กำลังตั้งค่ากระถางที่ "+str(pot))
    x = requests.post("http://localhost:5555/set_pot/"+str(pot)+"/"+mode_dict[str(mode)], json=obj)
    print(x.text)
    if x.text == "ok number one":
        await ctx.send("ตั้งค่าสำเร็จ")

@bot.command(pass_context = True , aliases=['พัดลม'])
async def fan(ctx, pot, do) :
    import requests
    dict_do = {
        "เปิด" : "on",
        "ปิด" : "off",
        "อัตโนมัติ" : "auto"
    }
    x = requests.get("http://localhost:5555/manual_fan/"+str(pot)+"/"+dict_do[do])
    result = x.json()
    if result["result"] == "error same":
        await ctx.send("ไม่สามารถทำคำสั่งที่ทำอยู่แล้ว")
    elif result["result"] == "Success":
        await ctx.send("พัดลมของกระถางที่"+ pot +" ถูกตั้งให้" + do)

@bot.command(pass_context = True , aliases=['รดน้ำ'])
async def manpump(ctx, pot) :
    import requests
    await ctx.send("คำสั่งรดน้ำอาจต้องรอถึง 10 วินาที...")
    x = requests.get("http://localhost:5555/man_pump/"+str(pot))
    result = x.json()
    if result["result"] == "error same":
        await ctx.send("ไม่สามารถทำคำสั่งที่กำลังทำ")
    elif result["result"] == "Success":
        await ctx.send("รดน้ำกระถางที่ " + pot + " แล้ว")
    elif result["result"] == "low water":
        await ctx.send("ไม่สามารถรดน้ำได้เนื่องจากมีปริมาณน้ำสะสมต่ำ")

bot.run('OTUyNDgyOTY0NTQ0MDU3MzU1.Yi2q4w.7RfEZINFF_0r2WyfBBRIDdLRA0U') #รันบอท (โดยนำ TOKEN จากบอทที่เราสร้างไว้นำมาวาง)
