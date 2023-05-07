import aiogram
import asyncio
from handlers import echo, admin, doctor, patient

bot = aiogram.Bot(token="6196065573:AAFASlJ9SFj-DTERibJV4omGRF0nF2BORBo")
dp = aiogram.Dispatcher()
dp.include_router(echo.router)
dp.include_router(admin.router)
dp.include_router(doctor.router)
dp.include_router(patient.router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
