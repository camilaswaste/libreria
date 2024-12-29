from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Creates the productos_autores table if it does not exist'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS `productos_autores` (
                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                `producto_id` bigint(20) NOT NULL,
                `autor_id` bigint(20) NOT NULL,
                PRIMARY KEY (`id`),
                UNIQUE KEY `productos_autores_producto_id_autor_id_unique` (`producto_id`,`autor_id`),
                KEY `productos_autores_autor_id_fk_autores_id` (`autor_id`),
                CONSTRAINT `productos_autores_autor_id_fk_autores_id` FOREIGN KEY (`autor_id`) REFERENCES `autores` (`id`),
                CONSTRAINT `productos_autores_producto_id_fk_productos_id` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)
        self.stdout.write(self.style.SUCCESS('Successfully created productos_autores table'))

