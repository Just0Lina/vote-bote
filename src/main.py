import gateway

from kernel import dp
from dal import DB
from aiogram.utils import executor

if __name__ == '__main__':
    executor.start_polling(dp)
