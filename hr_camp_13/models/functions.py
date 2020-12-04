

from odoo import api, fields, models,_
from datetime import datetime



class functions_to_attendance (models.Model):

    
    def init(self):
      self.env.cr.execute("""




-- FUNCTION: public.update_totalroomsoccupancy()

DROP FUNCTION  if exists public.update_totalroomsoccupancy() CASCADE;

CREATE FUNCTION public.update_totalroomsoccupancy()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$DECLARE
    tro integer;
    ntro    integer;
    otro    integer;
    free_beds integer;
BEGIN

IF (TG_OP = 'INSERT') THEN

    SELECT SUM(roomcapacity) INTO tro FROM camp_details_rooms WHERE campcode_id = new.campcode_id;
    SELECT tro - SUM(roomoccupancy) INTO free_beds FROM camp_details_rooms WHERE campcode_id = new.campcode_id;

    UPDATE camp_details SET totalroomoccupancy = tro,noofrooms=tro WHERE id = NEW.campcode_id;

ELSEIF (TG_OP = 'UPDATE') THEN

    ntro = NEW.roomcapacity;
    otro = OLD.roomcapacity;

    SELECT SUM(roomcapacity) INTO otro FROM camp_details_rooms WHERE campcode_id = OLD.campcode_id;

    UPDATE camp_details SET totalroomoccupancy = otro WHERE id = OLD.campcode_id;

    SELECT SUM(roomcapacity) INTO ntro FROM camp_details_rooms WHERE campcode_id = NEW.campcode_id;
    SELECT ntro-SUM(roomoccupancy) INTO free_beds FROM camp_details_rooms WHERE campcode_id = NEW.campcode_id;

    UPDATE camp_details SET totalroomoccupancy = ntro,noofrooms=free_beds WHERE id = NEW.campcode_id;

ELSEIF (TG_OP = 'DELETE') THEN

    otro = OLD.roomcapacity;

    SELECT SUM(roomcapacity) INTO otro FROM camp_details_rooms WHERE campcode_id = OLD.campcode_id;
    SELECT otro-SUM(roomoccupancy) INTO free_beds FROM camp_details_rooms WHERE campcode_id = old.campcode_id;

    UPDATE camp_details SET totalroomoccupancy = otro,noofrooms=free_beds WHERE id = OLD.campcode_id;

END IF;

RETURN NULL;

END;$BODY$;

ALTER FUNCTION public.update_totalroomsoccupancy()
    OWNER TO postgres;


-- FUNCTION: public.update_totalrooms()

DROP FUNCTION  if exists public.update_totalrooms() cascade;

CREATE FUNCTION public.update_totalrooms()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$DECLARE
    trms    integer;
BEGIN

IF (TG_OP = 'INSERT') THEN

    SELECT COUNT(id) INTO trms FROM camp_details_rooms WHERE campcode_id = NEW.id;

    UPDATE camp_details SET totalrooms = trms WHERE id = NEW.id;

ELSEIF (TG_OP = 'UPDATE') THEN

    SELECT COUNT(id) INTO trms FROM camp_details_rooms WHERE campcode_id = OLD.id;

    IF (OLD.totalrooms <> trms) THEN

        UPDATE camp_details SET totalrooms = trms WHERE id = OLD.id;
    
    END IF;

END IF;
RETURN NULL;
END;$BODY$;

ALTER FUNCTION public.update_totalrooms()
    OWNER TO postgres;

-- FUNCTION: public.transfer_room_camp()

DROP FUNCTION  if exists  public.transfer_room_camp() cascade;

CREATE FUNCTION public.transfer_room_camp()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$declare
total_occ integer;
tro integer;
free_beds integer;
Begin 
   UPDATE hr_employee  SET room_ids  = New.trn_room , camp_ids= New.camp_no where hr_employee.id=New.emp_name;
   select count(id) into total_occ from hr_employee where room_ids  = New.trn_room;
   UPDATE camp_details_rooms set roomoccupancy=total_occ where id=New.trn_room;
   UPDATE camp_details_rooms set roomoccupancy=roomoccupancy -1 where id=New.cur_room;
   
    SELECT SUM(roomcapacity) INTO tro FROM camp_details_rooms WHERE campcode_id = new.camp_no;
    SELECT SUM(roomoccupancy) INTO free_beds FROM camp_details_rooms WHERE campcode_id = new.camp_no;
    UPDATE camp_details SET totalroomoccupancy = tro,totaloccupants=free_beds WHERE id = NEW.camp_no;

    SELECT SUM(roomcapacity) INTO tro FROM camp_details_rooms WHERE campcode_id = new.camp_cur;
    SELECT SUM(roomoccupancy) INTO free_beds FROM camp_details_rooms WHERE campcode_id = new.camp_cur;
    UPDATE camp_details SET totalroomoccupancy = tro,totaloccupants=free_beds WHERE id = new.camp_cur;

   
   RETURN NULL;
End;
$BODY$;

ALTER FUNCTION public.transfer_room_camp()
    OWNER TO postgres;

-- Trigger: udpate_totalrooms

-- DROP TRIGGER udpate_totalrooms ON public.camp_details;

CREATE TRIGGER udpate_totalrooms
    AFTER INSERT OR UPDATE 
    ON public.camp_details
    FOR EACH ROW
    EXECUTE PROCEDURE public.update_totalrooms();

    -- Trigger: update_totalroomoccupancy

-- DROP TRIGGER update_totalroomoccupancy ON public.camp_details_rooms;

CREATE TRIGGER update_totalroomoccupancy
    AFTER INSERT OR DELETE OR UPDATE 
    ON public.camp_details_rooms
    FOR EACH ROW
    EXECUTE PROCEDURE public.update_totalroomsoccupancy();

    -- Trigger: Update_employee_occupation

-- DROP TRIGGER "Update_employee_occupation" ON public.camp_transfer;

CREATE TRIGGER "Update_employee_occupation"
    AFTER INSERT OR UPDATE 
    ON public.camp_transfer
    FOR EACH ROW
    EXECUTE PROCEDURE public.transfer_room_camp();



    """)


