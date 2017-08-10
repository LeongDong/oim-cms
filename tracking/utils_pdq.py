from __future__ import absolute_import
from datetime import datetime
from django.utils import timezone
import os
import unicodecsv
from uuid import UUID

from .models import Computer
from .utils import logger_setup


def csv_data(csv_path, skip_header=True):
    """Pass in the path to a CSV file, returns a CSV Reader object.
    """
    csv_file = open(csv_path, 'r')
    # Determine the CSV dialect.
    dialect = unicodecsv.Sniffer().sniff(csv_file.read(1024))
    csv_file.seek(0)
    data = unicodecsv.reader(csv_file, dialect)
    if skip_header:
        data.next()
    return data


def pdq_load_computers():
    """Update the database with Computer information from PDQ Inventory.
    """
    logger = logger_setup('pdq_load_computers')
    logger_ex = logger_setup('exceptions_pdq_load_computers')
    update_time = timezone.now()
    csv_path = os.path.join(os.environ.get('PDQ_INV_PATH'), 'pdq_computers.csv')
    data = csv_data(csv_path)
    num_created = 0
    num_updated = 0
    num_errors = 0

    for row in data:
        try:
            computer = None
            try:
                urn = UUID(row[2]).urn
            except Exception as e:
                logger_ex.error('Computer {} has invalid Active Directory GUID in PDQ Inventory {}, skipping.'.format(row[1], row[2]))
                logger_ex.info(row)
                logger_ex.exception(e)
                num_errors += 1
                continue

            # First, try and match AD GUID.
            if urn and row[2]:
                try:
                    computer = Computer.objects.get(ad_guid=urn)
                    num_updated += 1
                except Computer.DoesNotExist:
                    pass
            # Second, try and match AD DN.
            if computer is None and row[3]:
                try:
                    computer = Computer.objects.get(ad_dn=row[3])
                    num_updated += 1
                except Computer.DoesNotExist:
                    pass
            # Last, try to match via sAMAccountName. If no match, skip the record.
            if computer is None:
                sam = '{}$'.format(row[1].upper())
                try:
                    computer = Computer.objects.get(sam_account_name=sam)
                    num_updated += 1
                except Computer.DoesNotExist:
                    logger.info('No match for Computer object with SAM ID {} creating new object'.format(sam))
                    computer = Computer(sam_account_name=sam)
                    num_created += 1
                    pass

            computer.domain_bound = True
            computer.hostname = row[17]
            computer.pdq_id = int(row[0])
            computer.ad_guid = urn
            computer.ad_dn = row[3]
            computer.manufacturer = row[5]
            computer.model = row[6]
            computer.chassis = row[7]
            computer.serial_number = row[8]
            computer.os_name = row[9]
            computer.os_version = row[10]
            computer.os_service_pack = row[11]
            computer.os_arch = row[12]
            computer.cpu = row[13]
            computer.cpu_count = row[14]
            computer.cpu_cores = row[15]
            computer.memory = row[16]
            computer.date_pdq_updated = update_time
            computer.save()
            logger.info('Computer {} updated from PDQ Inventory scan data'.format(computer))
        except Exception as e:
            logger_ex.error('Error while loading computers from PDQ')
            logger_ex.info(row)
            logger_ex.exception(e)
            num_errors += 1
            continue

    logger.info('Created {}, updated {}, errors {}'.format(num_created, num_updated, num_errors))


def pdq_load_logins():
    """Update Computers with 'last login' information from PDQ Inventory.
    """
    logger = logger_setup('pdq_load_logins')
    csv_path = os.path.join(os.environ.get('PDQ_INV_PATH'), 'pdq_logins.csv')
    data = csv_data(csv_path)
    num_updated = 0
    num_skipped = 0

    for row in data:
        # Match on sAMAccountName only.
        if Computer.objects.filter(sam_account_name__istartswith=row[3]).exists():
            computer = Computer.objects.filter(sam_account_name__istartswith=row[3])[0]
            if row[2]:
                computer.last_ad_login_username = row[2]
            if row[1]:
                ts = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                computer.last_ad_login_date = ts.date()
            computer.save()
            logger.info('Computer {} login data updated'.format(computer))
            num_updated += 1
        else:
            logger.warning('Hostname {} did not match any Computer'.format(row[3]))
            logger.info(row)
            num_skipped += 1

    logger.info('Updated {}, skipped {}'.format(num_updated, num_skipped))
